import os
import subprocess

from argparse import ArgumentParser
from time import sleep

class Log():
    @classmethod
    def debug(cls, message): # only for now, latter i will build better with colors
        print(f"[DEBUG] {message}")

    @classmethod
    def error(cls, message):
        print(f"[ERROR] {message}")

    @classmethod
    def section_pause(cls):
        print("#"*30)
class GitSetup(object):

    def run_git_cmd(self):
        subprocess.call("git config --global --list")
        subprocess.call("git ")

    def setup_user(self):
        pass


class Utils(object):

    def get_cmd_arguments(self, dict_args):
        parser = ArgumentParser()
        # TODO implement this badboy with parsing dict of arguments


class SubprocessPlayground(object):
    """
        Running shell scripts / commands with usage of subprocesses
        run | call | popen differ in how execute command and
            how they manage output and return codes

        Multiprocessing is for parallel execution of processes
        subprocess is manage external processes like ping ls make and more
        to run multiple command using subprocess we can use pipes

        subprocess - module to running child-processes - means external programs
        usually we use subprocess.run and Popen - to have more control
            call is deprecated and unused so we are not going to learn this badboy
    """

    def simple_run(self, ):
        result = subprocess.run([
            "wsl",   # wsl because iam on windows now
            "echo",
            "What's going on in here"
        ])
        Log.debug(f"Result: {result.returncode}")

    """
        run with capture_output set to True will load stdout
            and stderr if there occurs ones 
    """
    def run_with_capture(self):
        output = subprocess.run([
            "wsl",
            "echo",
            "Am I going to be captured?"
        ],
            capture_output=True,
            text=True
        )
        if output.returncode == 0 :
            Log.debug(f"Captured text: {output.stdout} // Yes You do.")
        else:
            Log.debug(f"Captured errors: {output.stderr} // There is a problem in here.")

    """
      run with check=True will raise an exception with Error 
        returncode and std-out|err if there will be providen
    """
    def run_with_exception(self):
        try:
            subprocess.run(["wsl", "ls", "/notFound"], check=True)
        except subprocess.CalledProcessError as subException:
            Log.error(f"Process Error captured: ${subException}")
            Log.error(f"Return Code: ${subException.returncode}")

    """
        Popen - starts given process and return the process object
            communicate - waits until the process ends and return std-out|err
            manually running proces
            its not waiting until process end its return hock to the process
        
        subprocess.PIPE- instead of putting result to consol it
            contects pipe, to make it by youself
    """
    def simple_popen(self):
        process = subprocess.Popen(
            ["ping", "google.com", "-n", "2"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, err = process.communicate() # wait until process ends
        sleep(1)
        process.terminate() # killing bastard
        Log.debug(f"Out: {out}")
        Log.debug(f"Err: {err}")
        Log.debug(f"Pid: {process.pid} and code: {process.returncode}")


setup = GitSetup()
# setup.run_git_cmd()


sub_playground = SubprocessPlayground()
sub_playground.simple_run()
sub_playground.run_with_capture()
sub_playground.run_with_exception()
Log.section_pause()
sub_playground.simple_popen()