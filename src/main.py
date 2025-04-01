from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
import shutil
import os
import subprocess

app = FastAPI()

@app.post("/encrypt")
async def encrypt_file(background_tasks : BackgroundTasks, password: str = Form(...), outputFilename: str = Form(...), file: UploadFile = File(...)):
    # Get file set input file name, output file name and password
    inputFileName = file.filename
    outputFileName = outputFilename
    password = password
    tmpPath = "/tmp/"
    print("Input file name: " + inputFileName)
    print("Output file name: " + outputFileName)
    #print("Password: " + password)

    
    # Save uploaded file
    with open(tmpPath + inputFileName, "wb") as buffer:
       shutil.copyfileobj(file.file, buffer)

    command = "gpg " 
    command += "--symmetric " 
    command += "--batch "
    command += "--passphrase " + password + " "
    command += "--s2k-mode 3 "
    command += "--s2k-count 65011712 "
    command += "--s2k-digest-algo SHA512 "
    command += "--s2k-cipher-algo AES256 "
    command += "--output " + tmpPath + outputFileName + " "
    command += tmpPath + inputFileName

    #print("GPG command: " + command)

    subprocess.run(command, shell=True)
       
    # Cleanup and return decrypted file
    background_tasks.add_task(remove_file, tmpPath + inputFileName)
    background_tasks.add_task(remove_file, tmpPath + outputFileName)
    return FileResponse(tmpPath + outputFileName, media_type="application/octet-stream", filename=outputFileName)
        
@app.post("/decrypt")
async def decrypt_file(background_tasks : BackgroundTasks, password: str = Form(...), outputFilename: str = Form(...), file: UploadFile = File(...)):
    # Get file set input file name, output file name and password
    inputFileName = file.filename
    outputFileName = outputFilename
    password = password
    tmpPath = "/tmp/"
    print("Input file name: " + inputFileName)
    print("Output file name: " + outputFileName)
    #print("Password: " + password)

    # Save uploaded file
    with open(tmpPath + inputFileName, "wb") as buffer:
       shutil.copyfileobj(file.file, buffer)

    command = "gpg " 
    command += "--decrypt " 
    command += "--batch "
    command += "--passphrase " + password + " "
    command += "--output " + tmpPath + outputFileName + " "
    command += tmpPath + inputFileName

    print("GPG command: " + command)

    subprocess.run(command, shell=True)
       
    # Cleanup and return decrypted file
    background_tasks.add_task(remove_file, tmpPath + inputFileName)
    background_tasks.add_task(remove_file, tmpPath + outputFileName)
    return FileResponse(tmpPath + outputFileName, media_type="application/octet-stream", filename=outputFileName)
   


# remove files after delivery files back
def remove_file(path: str) -> None:
    if os.path.exists(path):
      os.remove(path)
    
