import time
import threading


class DischargeThread(threading.Thread):
    def __init__(self, settings, command):
        super(DischargeThread, self).__init__()
        self.settings = settings
        self.command = command
        self.status = True
        self.history = []
        self.stop = False
        self._stop_event = threading.Event()

    def get_history(self):
        return self.history

    def stop_thread(self):
        print('STOP_THREAD')
        self._stop_event.set()

    def get_data_from_discharge(self, down):
        down_changer = down
        temp_trigger = True
        status = {'v': 85, 't': 22}
        temp = status['t']
        volt = status['v']

        while volt > self.settings['discharged'] and temp_trigger == True:
            yield f"v: {volt}, t{temp}"
            volt -= down_changer
            temp += down_changer
            if temp >= 70:
                self.stop_thread()
                self.command.stop_command(self.history)
            # elif temp >= 50:
            #     down_changer = round((down_changer * 0.7), 1)
            #     temp -= round((down_changer * 2), 1)
            # TODO zakomentowane aby przekroczyć temperature
            else:
                down_changer = down

            time.sleep(0.5)

    def start_discharge(self):
        for status in self.get_data_from_discharge(self.settings['step']):
            print(status, self.stop)
            self.history.append(status)
            if self._stop_event.is_set():
                print('stop')
                break

        print(self.history)
