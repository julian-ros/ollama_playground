## DESCRIPTION

The API will generate the vectorDB at init time from the `jsonl` files stored in the embeddings folder.
So far, this operation is required every time the API is instantiated. We need to explore how to reuse the pickle file generated so this step can be skipped. Currently takes 2 minutes to generate the pickel.

The HyperDB module is loaded from a public repo in the AIXOS organization due to some changes implemented in the project, which has been forked into our organization.

## SETUP

Set the required environment variables
```
export  OPENAI_API_KEY= {open_ai_key} 
```

Install the requirements

```
pip install -r requirements.txt
```

## EXECUTION

To run the API locally run from terminal

```
uvicorn src.__init__:app
```

API is exposed in endpoint:

```
[POST]http://127.0.0.1:8000/request-embeddings
```

Example request:

```
{
    "text": "Tell me about unreal 5.2 new features?"
}
```

