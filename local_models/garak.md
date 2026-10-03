
# Running garak’s jailbreak probe family. “DAN” (Do Anything Now) on the Phi-3

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

docker exec ollama ollama run phi3:mini

#list loaded models
docker exec ollama ollama list

# run only the jailbreak probe category
python -m garak --model_type ollama --model_name phi3:mini --probes dan
```