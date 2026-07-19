

## Ollama runtime

* Use Ollama server to pull, run, and manage models:
    *  For GPU acceleration you'd also need `--gpus=all` (NVIDIA) plus the NVIDIA Container Toolkit installed on the hostm otherwise it falls back to CPU ONLY INFERENCE 

* Ollama [library for models](https://ollama.com/library)

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

* Pull the desired model

```bash
docker exec ollama ollama run phi3
```

* Prompt the model

```bash
docker exec -it ollama ollama run phi3 "PROMPT"

docker exec -it ollama ollama run phi3 "if __name__ =="
docker exec -it ollama ollama run phi3 "weather forecast now"

```
