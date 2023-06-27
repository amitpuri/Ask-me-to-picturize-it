import wikipedia
import requests
import json
from langchain.prompts import PromptTemplate

class AskPicturizeIt:
    TITLE = '# [Ask-picturize-it](https://github.com/amitpuri/Ask-picturize-it)'
    DESCRIPTION = """<strong>This space uses following:</strong>
       <p>
       <ul>    
       <li>OpenAI API Whisper(whisper-1) <a href='https://openai.com/research/whisper'>https://openai.com/research/whisper</a></li>    
       <li>DALL-E <a href='https://openai.com/product/dall-e-2'>https://openai.com/product/dall-e-2</a></li>
       <li>GPT(gpt-3.5-turbo) <a href='https://openai.com/product/gpt-4'>https://openai.com/product/gpt-4</a></li>  
       <li>Azure OpenAI <a href='https://azure.microsoft.com/products/cognitive-services/openai-service'>https://azure.microsoft.com/products/cognitive-services/openai-service</a></li>  
       <li>Cloudinary <a href='https://cloudinary.com/documentation/python_quickstart'>https://cloudinary.com/documentation/python_quickstart</a></li>
       <li>Gradio App <a href='https://gradio.app/docs'>https://gradio.app/docs</a> in Python and MongoDB</li>
       <li>Prompt optimizer <a href='https://huggingface.co/microsoft/Promptist'>https://huggingface.co/microsoft/Promptist</a></li>
       <li>stabilityai/stable-diffusion-2-1 <a href='https://huggingface.co/stabilityai/stable-diffusion-2-1'>https://huggingface.co/stabilityai/stable-diffusion-2-1</a></li>
       <li>Stability AI <a href='https://stability.ai'>https://stability.ai</a></li>
       <li>LangChain OpenAI <a href='https://python.langchain.com/en/latest/modules/models/llms.html'>https://python.langchain.com/en/latest/modules/models/llms.html</a></li>
       <li>Article Extractor and Summarizer on Rapid API <a href='https://rapidapi.com'>https://rapidapi.com</a></li> 
       <li>A Python package to assess and improve fairness of machine learning models.<a href='https://fairlearn.org'>https://fairlearn.org</a></li>  
       </ul>
       </p>
     """
    RESEARCH_SECTION = """
       <p><strong>Check it out</strong></p>
       <p>
       <ul>
       <li><p>Attention Is All You Need <a href='https://arxiv.org/abs/1706.03762'>https://arxiv.org/abs/1706.03762</a></p></li>
       <li><p>NLP's ImageNet moment has arrived <a href='https://thegradient.pub/nlp-imagenet'>https://thegradient.pub/nlp-imagenet</a></p></li>   
       <li><p>Zero-Shot Text-to-Image Generation <a href='https://arxiv.org/abs/2102.12092'>https://arxiv.org/abs/2102.12092</a></p></li>   
       <li><p>Transformer: A Novel Neural Network Architecture for Language Understanding <a href='https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html'>https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html</a></p></li>
       <li><p>CS25: Transformers United V2 <a href='https://web.stanford.edu/class/cs25'>https://web.stanford.edu/class/cs25</a></p></li>
       <li><p>CS25: Stanford Seminar - Transformers United 2023: Introduction to Transformer <a href='https://youtu.be/XfpMkf4rD6E'>https://youtu.be/XfpMkf4rD6E</a></p></li>
       <li><p>Temperature in NLP <a href='https://lukesalamone.github.io/posts/what-is-temperature'>https://lukesalamone.github.io/posts/what-is-temperature</a></p></li>
       <li><p>openai-cookbook <a href='https://github.com/openai/openai-cookbook'>https://github.com/openai/openai-cookbook</a></p></li>              
       <li><p>Open LLM Leaderboard <a href='https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard'>https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard</a></p></li>
       <li><p>Aviary Explorer  <a href='https://aviary.anyscale.com'>https://aviary.anyscale.com</a></p></li>       
       <li><p>LangChain <a href='https://langchain.com/features.html'>https://langchain.com/features.html</a></p></li>
       <li><p>LangChain Python <a href='https://python.langchain.com'>https://python.langchain.com</a></p></li>
       <li><p>LangChain for Gen AI and LLMs <a href='https://www.youtube.com/playlist?list=PLIUOU7oqGTLieV9uTIFMm6_4PXg-hlN6F'>https://www.youtube.com/playlist?list=PLIUOU7oqGTLieV9uTIFMm6_4PXg-hlN6F</a></p></li>
       <li><p>LangChain's integration with Chroma <a href='https://blog.langchain.dev/langchain-chroma'>https://blog.langchain.dev/langchain-chroma</a></p></li>
       <li><p>Vector Similarity Explained <a href='https://www.pinecone.io/learn/vector-similarity'>https://www.pinecone.io/learn/vector-similarity</a></p></li>
       <li><p>An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale <a href='https://arxiv.org/abs/2010.11929'>https://arxiv.org/abs/2010.11929</a></p></li>
       <li>stable-diffusion-image-variations <a href='https://huggingface.co/spaces/lambdalabs/stable-diffusion-image-variations'>https://huggingface.co/spaces/lambdalabs/stable-diffusion-image-variations</a></li> 
       <li>text-to-avatar <a href='https://huggingface.co/spaces/lambdalabs/text-to-avatar'>https://huggingface.co/spaces/lambdalabs/text-to-avatar</a></li> 
       <li>generative-music-visualizer <a href='https://huggingface.co/spaces/lambdalabs/generative-music-visualizer'>https://huggingface.co/spaces/lambdalabs/generative-music-visualizer</a></li> 
       <li>text-to-pokemon <a href='https://huggingface.co/spaces/lambdalabs/text-to-pokemon'>https://huggingface.co/spaces/lambdalabs/text-to-pokemon</a></li> 
       <li>image-mixer-demo <a href='https://huggingface.co/spaces/lambdalabs/image-mixer-demo'>https://huggingface.co/spaces/lambdalabs/image-mixer-demo</a></li> 
       <li>Stable Diffusion <a href='https://huggingface.co/blog/stable_diffusion'>https://huggingface.co/blog/stable_diffusion</a></li> 
       <li>CoDi: Any-to-Any Generation via Composable Diffusion <a href='https://codi-gen.github.io'>https://codi-gen.github.io</a></li>        
       </ul>
       </p>
    """

    SECTION_FOOTER = """
       <p>Note: Only PNG is supported here, as of now</p>
       <p>Visit <a href='https://ai.amitpuri.com'>https://ai.amitpuri.com</a></p>
    """
    DISCLAIMER = """MIT License
    
    Copyright (c) 2023 Amit Puri
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    
    """
    FOOTER = """<div class="footer">
                        <p>by <a href="https://www.amitpuri.com" style="text-decoration: underline;" target="_blank">Amit Puri</a></p>
                </div>            
            """
    
    
    AWESOME_CHATGPT_PROMPTS = """
    Credits 🧠 Awesome ChatGPT Prompts <a href='https://github.com/f/awesome-chatgpt-prompts'>https://github.com/f/awesome-chatgpt-prompts</a>
    """
    
    
    PRODUCT_DEFINITION = "<p>Define a product by prompt, picturize it, get variations, save it with a keyword for later retrieval. Credits <a href='https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers'>https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers</a></p>"
    
    LABEL_GPT_CELEB_SCREEN = "Select, Describe, Generate AI Image, Upload and Save"

    NO_API_KEY_ERROR = "Review Configuration tab for keys/settings, OPENAI_API_KEY is missing or No input"

    NO_GOOGLE_PALM_AI_API_KEY_ERROR = "Review Configuration tab for keys/settings, PaLM Generative AI API Key (or GOOGLE_PALM_AI_API_KEY) is missing or No input"

    ENTER_A_PROMPT_IMAGE = "Please a prompt for image"
    
    PDF_OUTPUT_INFO = "PDF summarize Output info"
    
    TRANSCRIBE_OUTPUT_INFO = "Transcribe and summarize Output info"
    
    NO_API_KEY_ERROR_INVALID = "Review Configuration tab for keys/settings, OPENAI_API_KEY is invalid."
    
    NO_RAPIDAPI_KEY_ERROR = "Review Configuration tab for keys/settings, RAPIDAPI_KEY is missing or No input"
    
    TASK_EXPLANATION_EXAMPLES = ["""Your task is to help a marketing team create a description for a retail website of a product based on a technical fact sheet.
           
                                Write a product description based on the information provided in the technical specifications delimited by triple backticks."""]

    
    PRODUCT_DEF_QUESTION_EXAMPLES = ["Limit answer to 50 words", 
                                 "Limit answer to 100 words", 
                                 "Write the answer in bullet points",
                                 "Write the answer in 2/3 sentences",
                                 "Write the answer in one line TLDR with the fewest words"
                                ]

    ARTICLE_LINKS_EXAMPLES = ["https://time.com/6266679/musk-ai-open-letter", 
                              "https://futureoflife.org/open-letter/ai-open-letter",
                              "https://github.com/openai/CLIP",
                              "https://arxiv.org/abs/2103.00020",
                              "https://arxiv.org/abs/2302.14045v2",
                              "https://arxiv.org/abs/2304.04487",
                              "https://arxiv.org/abs/2212.09611",
                              "http://arxiv.org/abs/2305.02897",
                              "https://arxiv.org/abs/2305.00050",
                              "https://arxiv.org/abs/2304.14473",
                              "https://arxiv.org/abs/1607.06450",
                              "https://arxiv.org/abs/1706.03762",
                              "https://spacy.io/usage/spacy-101",
                              "https://developers.google.com/machine-learning/gan/gan_structure",
                              "https://thegradient.pub/nlp-imagenet",
                              "https://arxiv.org/abs/2102.12092",
                              "https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html",
                              "https://lukesalamone.github.io/posts/what-is-temperature",
                              "https://langchain.com/features.html",
                              "https://arxiv.org/abs/2010.11929",
                              "https://developers.google.com/machine-learning/gan/generative"]



    KEYWORD_EXAMPLES = sorted(["Stable Diffusion", "Zero-shot classification", "Generative AI based Apps ", 
                    "Foundation Capital FMOps ", "Foundational models AI", "Prompt Engineering", "Generative AI", 
        		    "Hyperparameter optimization","Embeddings Search","Convolutional Neural Network","Recurrent neural network",
                    "XGBoost Grid Search", "Random Search" , "Bayesian Optimization", "NLP", "GPT", "Vector Database",
                    "OpenAI embeddings","ChatGPT","Python LangChain LLM", "Popular LLM models", "Hugging Face Transformer",
                    "Confusion Matrix", "Feature Vector", "Gradient Accumulation","Loss Functions","Cross Entropy",
                    "Root Mean Square Error", "Cosine similarity", "Euclidean distance","Dot product similarity",
                    "Machine Learning","Artificial Intelligence","Deep Learning", "Neural Networks", "Data Science",
                    "Supervised Learning","Unsupervised Learning","Reinforcement Learning", "Natural Language Processing", 
                    "Data Mining", "Feature Extraction", "Dimensionality Reduction", "Ensemble Learning", "Transfer Learning",
                    "Decision Trees","Support Vector Machines", "Clustering","Regression", "Computer Vision", "Big Data",                   
                    "Language Models","Transformer","BERT","OpenAI","Text Generation","Text Classification",
                    "Chatbots","Summarization","Question Answering","Named Entity Recognition","Sentiment Analysis",
                    "Pretraining","Finetuning","Contextual Embeddings","Attention Mechanism","Reinforcement learning",
                    "Pinecone, a fully managed vector database", "Weaviate, an open-source vector search engine",
                    "Redis as a vector database","Qdrant, a vector search engine", "Milvus", "Embedding-based search",
                    "Chroma, an open-source embeddings store","Typesense, fast open source vector search", "Low-code No-code",
                    "Zilliz, data infrastructure, powered by Milvus", "Lexical-based search","Graph-based search"                            
                   ])


    prompt_character = PromptTemplate(
    input_variables=["character_name","program_name"],
    template="What is the name of the actor acted as {character_name} in {program_name}, answer without any explanation and return only the actor's name?")

    prompt_bond_girl = PromptTemplate(
    input_variables=["movie_name"],
    template="Who was Bond girl co-star in {movie_name}? answer without any explanation and return only the actor's name?")


    CELEB_SEARCH_QUESTIONS_EXAMPLES = [prompt_character.format(character_name="James Bond",program_name="Casino Royale"),
                        prompt_character.format(character_name="James Bond",program_name="Die Another Day"),
                        prompt_character.format(character_name="James Bond",program_name="Never Say Never Again"),
                        prompt_character.format(character_name="James Bond",program_name="Spectre"),
                        prompt_character.format(character_name="James Bond",program_name="Tomorrow Never Dies"),
                        prompt_character.format(character_name="James Bond",program_name="The World Is Not Enough"),
                        prompt_character.format(character_name="James Bond",program_name="Goldfinger"),

                        prompt_character.format(character_name="James Bond",program_name="Octopussy"),
                        prompt_character.format(character_name="James Bond",program_name="Diamonds Are Forever"),
                        prompt_character.format(character_name="James Bond",program_name="Licence to Kill"), 
                        prompt_character.format(character_name="Patrick Jane",program_name="The Mentalist"),
                        prompt_character.format(character_name="Raymond Reddington",program_name="The Blacklist"),
                        prompt_bond_girl.format(movie_name="Casino Royale"),
                        prompt_bond_girl.format(movie_name="GoldenEye"),
                        prompt_bond_girl.format(movie_name="Spectre"),
                        prompt_bond_girl.format(movie_name="Tomorrow Never Dies"),
                        prompt_bond_girl.format(movie_name="Goldfinger"),
                        prompt_bond_girl.format(movie_name="No Time to Die"),
                        prompt_bond_girl.format(movie_name="Octopussy"),
                        prompt_bond_girl.format(movie_name="The World Is Not Enough"),
                        prompt_bond_girl.format(movie_name="Diamonds Are Forever"),
                        prompt_bond_girl.format(movie_name="Licence to Kill"),                          	
		                prompt_bond_girl.format(movie_name="Die Another Day")]


    TEST_MESSAGE = """Rewrite this into a casual email:
        
Tis but thy name that is my enemy;
Thou art thyself, though not a Montague.
What’s Montague? It is nor hand, nor foot,
Nor arm, nor face, nor any other part
Belonging to a man. O, be some other name!
What’s in a name? That which we call a rose
By any other name would smell as sweet;
So Romeo would, were he not Romeo call’d,
Retain that dear perfection which he owes
Without that title. Romeo, doff thy name,
And for that name which is no part of thee
Take all myself."""

    
    def get_wikimedia_image(self, keyword):
        WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

        if keyword:
            try:
                result = wikipedia.search(keyword, results = 1)
            except wikipedia.exceptions.WikipediaException as exception:
                print(f"Exception Name: {type(exception).__name__}")
                print(exception)
                result = None
                pass
            wikipedia.set_lang('en')
            try:
                if result is not None:
                    try:
                        wkpage = wikipedia.WikipediaPage(title = result[0])
                    except:
                        print(result)
                    finally:
                        wkpage = None    
            except wikipedia.exceptions.WikipediaException as exception:
                print(f"Exception Name: {type(exception).__name__}")
                print(exception)
                wkpage = None
                pass
            if wkpage is not None:
                title = wkpage.title
                response  = requests.get(WIKI_REQUEST+title)
                json_data = json.loads(response.text)
                try:
                    image_link = list(json_data['query']['pages'].values())[0]['original']['source']
                    return image_link
                except:
                    return None
    
    def get_wiki_page_summary(self, keyword):
        if keyword:
            try:
                return wikipedia.page(keyword).summary
            except wikipedia.exceptions.PageError:
                return f"No page for this keyword {keyword}"
            except Exception as exception:
                print(f"Exception Name: {type(exception).__name__}")
                print(exception)