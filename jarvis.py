import os
import sys
import datetime
import webbrowser
import time
import re
import subprocess
import pyttsx3
import speech_recognition as sr

class JarvisAssistant:
    def __init__(self):
        print("[*] Initializing voice engine...")
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        
        # System speech engine setup (Selecting Russian voice package if available)
        for voice in self.voices:
            if "russian" in voice.name.lower() or "ru" in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        self.engine.setProperty('rate', 180)

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Wake word and session tracking parameters
        self.wake_words = ["джарвис", "джар", "jarvis"]
        self.is_active = False
        self.last_activation_time = 0

    def speak(self, text: str) -> None:
        """Outputs text notification via speech synthesis and console logging."""
        print(f"[Jarvis]: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_command(self) -> str:
        """Captures audio input and converts it into structured text string."""
        with self.microphone as source:
            if self.is_active:
                print("\n[Listening for command...] Speak now...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                command = self.recognizer.recognize_google(audio, language="ru-RU")
                return command.lower().strip()
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                return ""
            except sr.RequestError:
                self.speak("Проблема с доступом к сервису распознавания.")
                return ""

    def _set_windows_volume(self, level: int) -> None:
        """Internal helper utilizing Windows COM-layer scripts to alter audio mix levels."""
        level = max(0, min(100, level))
        os.system(f"powershell -Command \"$wsh = New-Object -ComObject WScript.Shell; for($i=0; $i -lt 50; $i++) {{ $wsh.SendKeys([char]174) }}; for($i=0; $i -lt {int(level/2)}; $i++) {{ $wsh.SendKeys([char]175) }}\"")

    def execute_command(self, raw_command: str) -> bool:
        """Core linguistic parsing engine that evaluates runtime operational directives."""
        if not raw_command:
            if self.is_active and (time.time() - self.last_activation_time > 7):
                print("[*] Dialogue session timeout. Returning to background wake mode...")
                self.is_active = False
            return True

        print(f"[Captured]: {raw_command}")
        has_wake_word = any(wake in raw_command for wake in self.wake_words)

        if not self.is_active and not has_wake_word:
            return True

        if has_wake_word:
            self.is_active = True
            self.last_activation_time = time.time()
            for wake in self.wake_words:
                raw_command = raw_command.replace(wake, "").strip()
            if not raw_command:
                self.speak("Да, Лев. Слушаю вас.")
                return True

        command = raw_command

        # 1. Advanced Volume Controls (With expanded keywords support)
        if any(word in command for word in ["громкость", "звук", "громче", "тише"]):
            digits = re.findall(r'\d+', command)
            if digits:
                target_volume = int(digits[0])
                self.speak(f"Устанавливаю громкость на {target_volume} процентов")
                self._set_windows_volume(target_volume)
            elif any(word in command for word in ["выключи", "выключить", "муте", "выкл"]):
                self.speak("Выключаю звук")
                os.system("powershell -Command \"(New-Object -ComObject WScript.Shell).SendKeys([char]173)\"")
            elif any(word in command for word in ["добавь", "прибавь", "громче", "повысь"]):
                self.speak("Делаю громче")
                os.system("powershell -Command \"(New-Object -ComObject WScript.Shell).SendKeys([char]175)\"")
            elif any(word in command for word in ["тише", "убавь", "снизь"]):
                self.speak("Делаю тише")
                os.system("powershell -Command \"(New-Object -ComObject WScript.Shell).SendKeys([char]174)\"")
            else:
                self.speak("На сколько процентов установить громкость?")
            self.is_active = False
            return True

        # 2. Application and Ecosystem Orchestration (Enhanced fuzz matching)
        elif any(word in command for word in ["открой", "запусти", "открыть", "запустить"]):
            if "калькулятор" in command:
                self.speak("Запускаю калькулятор")
                subprocess.Popen("calc.exe")
            elif "блокнот" in command:
                self.speak("Открываю блокнот")
                subprocess.Popen("notepad.exe")
            elif "браузер" in command:
                self.speak("Открываю браузер")
                webbrowser.open("https://google.com")
            elif any(word in command for word in ["гитхаб", "github", "git"]):
                self.speak("Открываю ваш профиль Гитхаб")
                webbrowser.open("https://github.com/lev173")
            elif "диспетчер" in command or "taskmgr" in command:
                self.speak("Открываю диспетчер задач")
                subprocess.Popen("taskmgr.exe")
            elif "youtube" in command or "ютуб" in command:
                self.speak("Открываю Ютуб")
                webbrowser.open("https://youtube.com")
            else:
                self.speak("Такое приложение не зарегистрировано в моей системе.")
            self.is_active = False
            return True

        # 3. Native File System Maintenance
        elif "корзину" in command or "корзина" in command or "очисти" in command:
            if any(word in command for word in ["очисти", "очистить"]):
                self.speak("Очищаю системную корзину")
                os.system("powershell -Command \"Clear-RecycleBin -Force -ErrorAction SilentlyContinue\"")
                self.is_active = False
                return True

        # 4. Web Intelligence API and Fallback Routing
        elif any(word in command for word in ["найди", "поиск", "что такое", "кто такой", "какая", "какой", "самый"]):
            search_query = command
            for filter_word in ["найди", "поиск", "что такое", "кто такой"]:
                search_query = search_query.replace(filter_word, "")
            search_query = search_query.strip()
            
            if search_query:
                self.speak(f"Ищу в Google: {search_query}")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
            else:
                self.speak("Что именно мне найти?")
            self.is_active = False
            return True

        # 5. Core Environment Metrics and Status
        elif "время" in command or "который час" in command:
            now = datetime.datetime.now().strftime("%H:%M")
            self.speak(f"Сейчас {now}")
            self.is_active = False
            
        elif "дата" in command or "какое число" in command:
            today = datetime.datetime.now().strftime("%d %B %Y")
            self.speak(f"Сегодня {today}")
            self.is_active = False

        elif "заблокируй" in command or "блокировка" in command or "экран" in command:
            self.speak("Блокирую компьютер")
            os.system("rundll32.exe user32.dll,LockWorkStation")
            self.is_active = False

        # 6. Session Disposal
        elif any(word in command for word in ["пока", "выключись", "стоп", "до свидания", "завершить"]):
            self.speak("До свидания, Лев. Отключаю системы.")
            return False
            
        else:
            self.speak("Команда не найдена в моей базе данных.")
            self.is_active = False
            
        return True

    def run(self):
        """Infinite tracking processing loop."""
        print("[*] Jarvis running in background wake-word mode...")
        active = True
        while active:
            command = self.listen_command()
            active = self.execute_command(command)

if __name__ == "__main__":
    try:
        assistant = JarvisAssistant()
        assistant.run()
    except Exception as e:
        print(f"Критический сбой: {e}")