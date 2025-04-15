@echo off
cd ..
echo Starting Ollama model (mistral) in the background...
start "" /B cmd /C "ollama run mistral"
timeout /t 5 > nul
echo Running Mistral grader script...
python src\grader_mistral_via_ollama.py > output_mistral.txt
echo Output saved to output_mistral.txt
pause
