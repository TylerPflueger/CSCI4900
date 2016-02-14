"""Imports."""
from tempfile import mkdtemp
from subprocess import call
import shutil
import glob
import os

tempDirectoryPath = mkdtemp(dir=".")
command = "mvn -q dependency:copy-dependencies " +\
    "-DcopyPom='true' -DoutputDirectory='" + tempDirectoryPath + "'"
call(command, shell=True)

currentDirectory = os.getcwd()
os.chdir(tempDirectoryPath)
for jarFilePath in glob.glob('*.jar'):
    print jarFilePath
    call('dosocs2 oneshot ' + jarFilePath, shell=True)

os.chdir(currentDirectory)
shutil.rmtree(tempDirectoryPath)
