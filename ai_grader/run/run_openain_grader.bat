@echo off
cd ..
echo Running OpenAI grader script with chat gpt api...
python src\grader_openai.py > output_openai.txt
echo Output saved to output_openai.txt
pause
