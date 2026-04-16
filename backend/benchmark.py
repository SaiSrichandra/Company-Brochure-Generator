"""
Benchmark: Parallel vs Sequential scraping with SeleniumBase.

Usage:
    python benchmark.py
    python benchmark.py --url https://example.com --links 5
"""

import time
import argparse
from multiprocessing import Pool, cpu_count
from bs4 import BeautifulSoup
import requests
from seleniumbase import SB


# --- Scraping function (one page) ---

def scrape_page_uc(url_obj):
    """Scrape a single URL using UC mode (sequential only)."""
    url = url_obj["url"]
    text = ""
    try:
        soup = BeautifulSoup(requests.get(url, timeout=15).content, "html.parser")
        title = soup.title.string if soup.title else ""
        text += title + "\n\n"
        with SB(uc=True, test=True, locale="en-US", headless2=True) as sb:
            sb.driver.uc_open_with_reconnect(url)
            sb.wait_for_element("body", timeout=5)
            page_text = sb.get_text("body")
            text += (page_text or "No content") + "\n\n"
    except Exception as e:
        text += f"Error: {e}\n\n"
    return text


def scrape_page_headless(url_obj):
    """Scrape a single URL using regular headless Chrome (safe for parallel)."""
    url = url_obj["url"]
    text = ""
    try:
        soup = BeautifulSoup(requests.get(url, timeout=15).content, "html.parser")
        title = soup.title.string if soup.title else ""
        text += title + "\n\n"
        with SB(headless=True) as sb:
            sb.open(url)
            sb.wait_for_element("body", timeout=5)
            page_text = sb.get_text("body")
            text += (page_text or "No content") + "\n\n"
    except Exception as e:
        text += f"Error: {e}\n\n"
    return text


# --- Collect links from homepage ---

def get_links(url, max_links):
    """Scrape the homepage and return up to max_links unique internal links."""
    print(f"Collecting links from {url} ...")
    links = []
    try:
        with SB(uc=True, test=True, locale="en-US", headless2=True) as sb:
            sb.driver.uc_open_with_reconnect(url)
            sb.wait_for_element("body", timeout=5)
            elements = sb.find_elements("a")
            seen = set()
            for el in elements:
                href = el.get_attribute("href")
                if href and href.startswith("http") and href not in seen:
                    seen.add(href)
                    links.append({"type": "page", "url": href})
                if len(links) >= max_links:
                    break
    except Exception as e:
        print(f"Error collecting links: {e}")
    print(f"Found {len(links)} links to benchmark.\n")
    return links


# --- Benchmark runners ---

def run_sequential(links):
    """Scrape all links one at a time using UC mode."""
    results = []
    for link_obj in links:
        results.append(scrape_page_uc(link_obj))
    return results


def run_parallel(links):
    """Scrape all links using multiprocessing Pool (regular headless Chrome)."""
    num_workers = min(len(links), max(cpu_count() - 1, 1))
    with Pool(processes=num_workers) as pool:
        results = pool.map(scrape_page_headless, links)
    return results


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Benchmark parallel vs sequential scraping")
    parser.add_argument("--url", default="https://openai.com", help="Homepage URL to scrape links from")
    parser.add_argument("--links", type=int, default=5, help="Number of links to scrape (default: 5)")
    args = parser.parse_args()

    links = get_links(args.url, args.links)
    if not links:
        print("No links found. Exiting.")
        return

    print(f"Benchmarking with {len(links)} links on {cpu_count()} CPU cores")
    print(f"Sequential uses UC mode (undetected Chrome)")
    print(f"Parallel uses regular headless Chrome (UC can't multiprocess)\n")
    print("=" * 60)

    # --- Sequential ---
    print("Running SEQUENTIAL scraping ...")
    start = time.perf_counter()
    seq_results = run_sequential(links)
    seq_time = time.perf_counter() - start
    print(f"Sequential: {seq_time:.2f}s  ({len(seq_results)} pages)\n")

    # --- Parallel ---
    print("Running PARALLEL scraping ...")
    start = time.perf_counter()
    par_results = run_parallel(links)
    par_time = time.perf_counter() - start
    print(f"Parallel:   {par_time:.2f}s  ({len(par_results)} pages)\n")

    # --- Results ---
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"  Links scraped : {len(links)}")
    print(f"  CPU cores     : {cpu_count()}")
    print(f"  Pool workers  : {min(len(links), max(cpu_count() - 1, 1))}")
    print()
    print(f"  Sequential    : {seq_time:.2f}s")
    print(f"  Parallel      : {par_time:.2f}s")
    print()
    if par_time > 0:
        speedup = seq_time / par_time
        print(f"  Speedup       : {speedup:.2f}x")
        if speedup > 1:
            print(f"  Parallel is {speedup:.2f}x faster")
        else:
            print(f"  Sequential is {1/speedup:.2f}x faster (parallel overhead > benefit)")
    print("=" * 60)


if __name__ == "__main__":
    main()
