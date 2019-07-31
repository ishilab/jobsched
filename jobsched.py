#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# jobshed.py - Simple Job Scheduler
#  Susumu Ishihara 2019/7/31
#

from subprocess import Popen, PIPE
import time

class JobScheduler:
    def __init__(self, max_procs, base_args, params_list, interval=1):
        self.max_procs = max_procs
        self.running_procs = []
        self.base_args = base_args
        self.params_list = list(reversed(params_list))
        self.interval = interval

    def add(self, args):
        if len(self.running_procs) < self.max_procs:
            str_args = list(map(str, args))
            proc = Popen([*self.base_args, *str_args], stdout=PIPE, stderr=PIPE)
            with open(str(proc.pid)+'.cmd', mode='w') as f:
                print(*self.base_args, *str_args, file=f)
            self.running_procs.append(proc)
            return True
        return False

    def show_status(self):
        print("Running: ", end='')
        for p in self.running_procs:
            print('{:d} '.format(p.pid), end='')
        print('')

    def finish_proc(self, proc, retcode):
        pid = proc.pid
        if retcode != 0:
            print('Process {:d} ended in error.'.format(pid))
        print('Finished: {:d}'.format(proc.pid))
        with open(str(proc.pid)+'.out', mode='w') as f:
            print(proc.stdout.read().decode(), end='', file=f)
        with open(str(proc.pid)+'.err', mode='w') as f:
            print(proc.stderr.read().decode(), end='', file=f)
        self.running_procs.remove(proc)

    def dequeue(self):
        args = self.params_list[-1]
        if self.add(args) == True:
            self.params_list.pop()
            return True
        return False

    def run(self):
        while self.params_list:
            if not self.dequeue():
                break
        while self.running_procs:
            self.show_status()            
            for proc in self.running_procs:
                retcode = proc.poll()
                if retcode is not None:
                    self.finish_proc(proc, retcode)
                    if self.params_list:
                        self.dequeue()
            time.sleep(self.interval)

def main_sample():
    params_list = [(2, "Tokyo"), (4, "Osaka"), (6,), (8,), (10, )]
    job_sched = JobScheduler(2, ('echo', 'Hello'), params_list)
    job_sched.run()

if __name__ == "__main__":
    main_sample()

