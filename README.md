# Openrouter Chat

Chat with several LLMs from CLI through the [OpenRouter API](https://openrouter.ai/).


### Descritption

The script can be used to chat with several Large Language Models through the free openrouter API.
Useful to quicly try out chat models from CLI without having to set up a dedicated environment. 



### Usage
To instantiate a chat with a given model:
```shell
python chat.py --model "name version size"
```

To check what are the available free models and the correct name to pass as arguments type:
```shell
python chat.py --mlist 
```



**Warning**: you have access to a limited number of requests with the free API.