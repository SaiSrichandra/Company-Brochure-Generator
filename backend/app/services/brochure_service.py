from openai import OpenAI
from bs4 import BeautifulSoup
import requests
from seleniumbase import SB
import json
from dotenv import load_dotenv
from app.core.config import settings
from multiprocessing import Pool, cpu_count

load_dotenv()

class Links():
    def __init__(self, url, name, client):
        self.url = url
        self.company_name = name
        self.client = client
        self.links = []
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        self.title = soup.title.string if soup.title else ''
        with SB(uc=True, test=True, locale="en-US", headless2=True) as sb:
            sb.driver.uc_open_with_reconnect(url)
            sb.wait_for_element("body", timeout=2)
            page_text = sb.get_text("body")
            self.text = page_text
            all_links = sb.find_elements("a")
            for link in all_links:
                href = link.get_attribute("href")
                if href:
                    self.links.append(href)
    
    def extract_useful_links(self):
        prompt_list = self.create_prompts()
        response = self.client.chat.completions.create(
            model = "gpt-4o",
            messages = prompt_list,
            response_format={"type" : "json_object"}
        )
        return response.choices[0].message.content
    
    def create_prompts(self):
        sp = self.system_prompt()
        up = self.user_prompt()
        return [sp,up]
    
    def system_prompt(self):
        sp = {"role" : "system", 
              "content" : """You are an AI assiatant that is part of a broader ecosystem which generates brochures for companies. Your task is to identify from a list of web links, which web links are useful for obtaining more information about a company, what it does, what do they stand for, their team, their products etc. that is useful for creating its brochure such as links that talk about the company and please remove unnecessary links like Terms and conditions, link to policies, links that point to the same page,  emails etc. You will be given a the company's name, list of all the links scrapped from a website of a company. Your output should be top 10 links that will be necessary to get important information about the company in the form of a JSON object 
Example output : {
                    links : [
                    {"type":"About", "url": "https://Link.aboutthecompany.com/somehting"
                    {"type":"Careers", "url" : "https://Link.somethinginthecomapny.some/anotherthing"
                    ]
                }

                """
              }
        return sp
    
    def user_prompt(self):
        u_con = f"The company with name {self.company_name} has the following links in its website:\n"
        if not self.links:
            self.links = [{"type": "Homepage" , "url" : self.url}]
        u_con += str(self.links)
        u_con += "\nPlease filter these links and give me the links which are useful to obtain information about the company and the output should be in the form of a JSON"
        up = {"role" : "user", "content" : u_con}
        return up

class ExploreLinks():
    def __init__(self, list_of_links):
        self.links = list_of_links
    
    def scrape_single_link(self, url_obj):
        complete_description = ''
        url = url_obj['url']
        soup = BeautifulSoup(requests.get(url_obj['url']).content, 'html.parser')
        title = soup.title.string if soup.title else ''
        complete_description += (title + '\n\n')
        with SB(uc=True, test=True, locale="en-US", headless2=True) as sb:
            sb.driver.uc_open_with_reconnect(url)
            sb.wait_for_element("body", timeout=2)
            page_text = sb.get_text("body")
            if page_text:
                complete_description += (page_text + '\n\n')
            else:
                complete_description += 'No details found on this link\n\n'
        return complete_description

    def explore_links(self):
        final_description = ''
        with Pool(processes=min(len(self.links), cpu_count() - 1)) as pool:
            results = pool.map(self.scrape_single_link, self.links)
        final_description = '\n'.join(results)
        return final_description

class AIBrochure():
    def __init__(self, desc, company_name, client):
        self.desc = desc
        self.company_name = company_name
        self.client = client
    
    def generate_brochure(self):
        prompt_list = self.create_prompts()
        response = self.client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = prompt_list,
            stream = False
        )
        # disp_text = ""
        # for chunk in stream :
        #     # os.system('cls' if os.name == 'nt' else 'clear')
        #     # disp_text += chunk.choices[0].delta.content or ''
            # print(chunk.choices[0].delta.content, end="", flush=True)
        return response.choices[0].message.content[12:-4]
    
    def create_prompts(self):
        sp = self.system_prompt()
        up = self.user_prompt()
        return [sp,up]
    
    def system_prompt(self):
        sp = {"role" : "system", "content" : """You are an expert AI-powered content designer, brand strategist, and brochure creator. I want your help to generate a beautiful, professionally written and visually compelling brochure for a company using raw textual content scraped or collected from the company's website. I will provide you with long-form or unstructured content from multiple pages of the company's site. Your task is to:\n> - Analyze and extract the most important and representative content (e.g., About Us, Products/Services, Vision, Clients, Contact Info)\n> - Rewrite and organize the content into polished, concise, and well-structured brochure sections\n> - Maintain a tone that reflects the company's brand identity (professional, innovative, luxury, etc.)\n> - Format the output into brochure-friendly layout sections (headlines, subheadings, body text, taglines, CTAs)\n> - USe an appealing layout structure that would suit the company's brand and content. Give an output in the form of Markdown and no unnecessary text at all and no recommendations"
                Example Output : 

              ## Welcome to XXXX
                Experience technology designed for a new generation. 

              """}
        return sp
    
    def user_prompt(self):
        if self.desc is not None:
            desc_in = self.desc
        else:
            desc_in = 'Cannot scrape any details fromt this company'
        u_con = f"The name of company is {self.company_name} and has the following description:\n"
        u_con += desc_in
        u_con += "\n Please create an elegant company brochure with suitable headings and layout and provide an output in the form of Markdown\n"
        up = {"role" : "user", "content" : u_con}
        return up

def generate_brochure_text(company_name, url):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    links = Links(url, company_name, client).extract_useful_links()
    if len(json.loads(links)["links"]) > 0:
        give_link = json.loads(links)["links"]
    else:
        give_link = [{"type":"Homepage","url":str(url)}]

    complete_desc = ExploreLinks(give_link).explore_links()
    return AIBrochure(complete_desc, company_name, client).generate_brochure()

