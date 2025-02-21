import requests
import json
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

#OPENROUTER_API_KEY = "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"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_KEY")


def get_model_id(model_name:str = "", print_list = False):
    """ Map model name to id.
    Aguments:
      model_name. Name in the format: name-version-size (e.g. llama 3.2 1b instruct)
      print_list[optional]: Print the list of available models
    return: openrouter model id
    """
    
    #get the list of models names and store the free models
    models = requests.get(url = "https://openrouter.ai/api/v1/models").json()
    free_models = [i for i in models["data"] if "free" in i["name"]]
    #parse the name to get the id mapping name:id
    #TODO check all the name not taken by this method and adjust it (es. check deepseek r1)
    models_id = {model["name"].split(":")[-1].lower().replace(" (free)", "").strip() : model["id"] for model in free_models}
    
    #print the list of available models
    if print_list:
        print("You can call one of the following models:\n")
        for i in models_id:
            print(i)
        exit() #TODO give the opportunity to insert the name awithout exit the program
    
    #check if model name is correct and map it to the correct model id
    if model_name:
        try:
            return models_id[model_name]
        except:
            print("The name you passed is not valid. Check the list of available models correct names by passing --mlist on CLI.")
    else:
        print("Empty model name. Please provide a valid model name.")



#helper to send requests to the api provider
def chat(user_prompt:str, model_id):
    response = requests.post(
                            url="https://openrouter.ai/api/v1/chat/completions",
                            headers={
                                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                            },
                            data=json.dumps({
                                "model": model_id, 
                                "messages": [
                                {
                                    "role": "user",
                                    "content": f"{user_prompt}"
                                }
                                ]
                            })
                            )
    return response.json()["choices"][0]["message"]["content"]

#chat with the model untill loop is broken
def main(model_id):
    model_id = get_model_id(args.model)
    print(f"***You are talking with {model_id} via  the OpenRouter API***\n\n")
    while True:
        user_input = input("\n\033[92mUser:\033[0m ")
        try:
            response = chat(user_input, model_id)
            
            print(f"\n\33[35mAssistant:\033[0m {response}")
        except KeyboardInterrupt:
            print(f"Assistant: Bye, Bye!")
            break


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", help = "Model name in the format (all lower): {name} {version} {size}.\n E.g. llama 3.2. 1b instruct")
    parser.add_argument("--mlist", "-ml", help = "Get the list of available free models with the open router api", action = "store_true")
    args = parser.parse_args()
    parser.print_help()
    
    if args.mlist:
        get_model_id(print_list=True)
        
    model_id = get_model_id(args.model)
    print(f"***You are talking with {model_id} via  the OpenRouter API***\n\n")
    
    #launch the main chat
    main(model_id)
    
    
    # while True:
    #     user_input = input("\n\033[92mUser:\033[0m ")
    #     try:
    #       response = chat(user_input)
          
    #       print(f"\n\33[35mAssistant:\033[0m {response}")
    #     except KeyboardInterrupt:
    #         print(f"Assistant: Bye, Bye!")
    #         break