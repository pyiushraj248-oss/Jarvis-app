import os
import json
import random
import datetime
import time
import difflib

# --- यूज़र की सेटिंग्स ---
user_name = "बॉस"

# --- ऐप्स की डिक्शनरी (Activity Name के साथ) ---
app_dict = {
    "whatsapp": "com.whatsapp/com.whatsapp.HomeActivity",
    "instagram": "com.instagram.android/com.instagram.android.activity.MainTabActivity",
    "youtube": "com.google.android.youtube/com.google.android.apps.youtube.app.WatchWhileActivity",
    "facebook": "com.facebook.katana/com.facebook.katana.activity.FbMainTabActivity",
    "free fire": "com.dts.freefiremax/com.dts.freefiremax.MainActivity",
    "chrome": "com.android.chrome/com.google.android.apps.chrome.Main",
    "spotify": "com.spotify.music/com.spotify.music.MainActivity",
    "camera": "com.android.camera/com.android.camera.Camera"
}

# --- संपर्कों की डिक्शनरी ---
contacts = {
    "rahul": "919876543210",
    "amit": "919123456789",
    "mom": "919988776655",
    "papa": "919887766554",
    "mummy": "919988776655"
}

def speak(text, emotion="normal"):
    print("Jarvis:", text)
    if emotion == "happy":
        params = "-p 1.3 -r 1.2"
    elif emotion == "sad":
        params = "-p 0.8 -r 0.8"
    elif emotion == "excited":
        params = "-p 1.4 -r 1.3"
    else:
        params = "-p 1.0 -r 1.0"
    os.system(f'termux-tts-speak {params} "{text}"')

# --- याद रखने वाली फाइल (Memory) ---
MEMORY_FILE = "jarvis_brain.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"facts": {}, "history": []}

def save_brain(brain):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(brain, f, ensure_ascii=False, indent=4)

# --- 🧠 स्मार्ट चैट और मेमोरी ---
def smart_reply(user_input, brain):
    if "याद रखो" in user_input or "remember" in user_input:
        fact = user_input.replace("याद रखो", "").replace("remember", "").strip()
        brain["facts"]["general"] = fact
        save_brain(brain)
        return "ठीक है बॉस, मैंने याद रख लिया।", "happy"

    if "मेरा नाम" in user_input or "मेरा बर्थडे" in user_input or "birthday" in user_input:
        if "birthday" in brain["facts"]:
            return f"आपका बर्थडे {brain['facts']['birthday']} है ना बॉस?", "happy"
        elif "name" in brain["facts"]:
            return f"आपका नाम {brain['facts']['name']} है ना बॉस?", "happy"
        else:
            return "माफ़ कीजिए बॉस, मुझे यह नहीं पता। आप 'याद रखो मेरा बर्थडे...' बोलकर बता सकते हैं।", "normal"

    if "खुश" in user_input or "happy" in user_input or "मज़ा" in user_input:
        return "वाह! यह तो बहुत अच्छी बात है बॉस।", "happy"
    if "उदास" in user_input or "sad" in user_input or "टेंशन" in user_input:
        return "अरे बॉस, टेंशन मत लीजिए। मैं हूँ ना आपके साथ।", "sad"
    if "गुस्सा" in user_input or "angry" in user_input:
        return "शांत हो जाइए बॉस। गहरी सांस लीजिए।", "angry"
    if "कैसे हो" in user_input or "क्या हाल" in user_input or "how are you" in user_input:
        return "मैं तो मस्त हूँ बॉस! आप सुनाइए, आज क्या कर रहे हैं?", "happy"
    if "तुम्हारा नाम" in user_input or "your name" in user_input:
        return "मेरा नाम जार्विस है! आपने ही तो यह नाम रखा था।", "happy"
    
    if any(word in user_input for word in ["क्या है", "कौन है", "कहाँ है", "what is", "who is"]):
        try:
            import wikipedia
            query = user_input.replace("क्या है", "").replace("कौन है", "").replace("what is", "").replace("who is", "").strip()
            if query:
                summary = wikipedia.summary(query, sentences=2)
                return summary, "happy"
        except Exception:
            pass

    return None, "normal"

# --- प्रोग्राम शुरू ---
print("===================================")
print("       SMART JARVIS ASSISTANT      ")
print("===================================")

brain = load_brain()
speak(f"नमस्ते! मैं जार्विस हूँ। अब मैं आपके फोन को भी कंट्रोल कर सकता हूँ। बताइए बॉस?")

jokes = [
    "टीचर: तुम होमवर्क क्यों नहीं करते? स्टूडेंट: क्योंकि मैं आलसी हूँ।",
    "पत्नी: सुनो जी, मुझे कुछ कहना है। पति: ठीक है, कल बताना, आज मैच चल रहा है।"
]

while True:
    print("\n🎤 सुन रहा हूँ... (बोलिए)")
    result = os.popen("termux-speech-to-text").read().strip().lower()

    if not result or "error" in result:
        time.sleep(1)
        continue

    print("आपने कहा:", result)
    reply = ""
    emotion = "normal"
    app_matched = False

    brain["history"].append({"time": str(datetime.datetime.now()), "command": result})
    if len(brain["history"]) > 50: brain["history"].pop(0)
    save_brain(brain)

    # ==========================================
    # 1. बाहर निकलना (Exit)
    # ==========================================
    if "exit" in result or "बंद करो" in result or "bye" in result:
        speak(f"चलिए, फिर मिलते हैं। अपना ध्यान रखिएगा {user_name}!", "sad")
        break

    # ==========================================
    # 2. सिस्टम कंट्रोल (System Control) - नया फीचर
    # ==========================================
    
    # टॉर्च
    if "टॉर्च ऑन" in result or "torch on" in result or "light on" in result:
        os.system("termux-torch on")
        speak("टॉर्च ऑन कर दी बॉस।", "happy")
        time.sleep(1); continue
    elif "टॉर्च ऑफ" in result or "torch off" in result or "light off" in result:
        os.system("termux-torch off")
        speak("टॉर्च बंद कर दी बॉस।", "normal")
        time.sleep(1); continue

    # आवाज़ (Volume)
    elif "volume up" in result or "आवाज़ बढ़ाओ" in result:
        os.system("input keyevent 24") # Volume Up Keyevent
        speak("आवाज़ बढ़ा दी बॉस।", "normal")
        time.sleep(1); continue
    elif "volume down" in result or "आवाज़ कम" in result:
        os.system("input keyevent 25") # Volume Down Keyevent
        speak("आवाज़ कम कर दी बॉस।", "normal")
        time.sleep(1); continue
    elif "mute" in result or "साइलेंट" in result:
        os.system("input keyevent 164") # Mute Keyevent
        speak("फोन साइलेंट कर दिया बॉस।", "normal")
        time.sleep(1); continue

    # म्यूजिक कंट्रोल
    elif "play music" in result or "गाना चलाओ" in result:
        os.system("input keyevent 85") # Play/Pause Keyevent
        speak("म्यूजिक प्ले कर रहा हूँ बॉस।", "happy")
        time.sleep(1); continue
    elif "pause music" in result or "गाना रोको" in result:
        os.system("input keyevent 85") # Play/Pause Keyevent
        speak("म्यूजिक पॉज़ कर दिया बॉस।", "normal")
        time.sleep(1); continue
    elif "next song" in result or "अगला गाना" in result:
        os.system("input keyevent 87") # Next Track Keyevent
        speak("अगला गाना चला रहा हूँ।", "happy")
        time.sleep(1); continue

    # ब्राइटनेस
    elif "brightness full" in result or "ब्राइटनेस बढ़ाओ" in result:
        os.system("termux-brightness 255")
        speak("ब्राइटनेस पूरी कर दी बॉस।", "normal")
        time.sleep(1); continue
    elif "brightness low" in result or "ब्राइटनेस कम" in result:
        os.system("termux-brightness 50")
        speak("ब्राइटनेस कम कर दी बॉस।", "normal")
        time.sleep(1); continue

    # वाइब्रेशन
    elif "vibrate" in result or "वाइब्रेट" in result:
        os.system("termux-vibrate -d 1000")
        speak("फोन वाइब्रेट कर रहा हूँ बॉस।", "normal")
        time.sleep(1); continue

    # WiFi और Bluetooth (Settings खोलकर)
    elif "wifi" in result or "वाईफाई" in result:
        os.system("am start -a android.settings.WIFI_SETTINGS")
        speak("WiFi की सेटिंग्स खोल रहा हूँ बॉस।", "normal")
        time.sleep(2); continue
    elif "bluetooth" in result or "ब्लूटूथ" in result:
        os.system("am start -a android.settings.BLUETOOTH_SETTINGS")
        speak("Bluetooth की सेटिंग्स खोल रहा हूँ बॉस।", "normal")
        time.sleep(2); continue

    # स्क्रीन लॉक
    elif "lock phone" in result or "फोन लॉक" in result:
        os.system("input keyevent 26") # Power button
        speak("फोन लॉक कर दिया बॉस।", "normal")
        time.sleep(1); continue

    # ==========================================
    # 3. ऐप खोलना और बंद करना
    # ==========================================
    is_closing = any(word in result for word in ["बंद", "close", "band", "kill"])
    for app_name, package_name in app_dict.items():
        if app_name in result or difflib.get_close_matches(app_name, result.split(), n=1, cutoff=0.6):
            app_matched = True
            if is_closing:
                speak(f"{app_name} को बंद कर रहा हूँ बॉस...", "normal")
                os.system(f"am force-stop {package_name.split('/')[0]}")
                os.system("input keyevent 3")
            else:
                speak(f"{app_name} खोल रहा हूँ बॉस...", "happy")
                if "/" in package_name:
                    os.system(f"am start -n {package_name}")
                else:
                    os.system(f"am start -p {package_name}")
            time.sleep(3)
            break

    if app_matched:
        continue

    # ==========================================
    # 4. फोन कॉल और WhatsApp
    # ==========================================
    if "call" in result or "कॉल" in result:
        target_name = None
        for name in contacts.keys():
            if name in result or difflib.get_close_matches(name, result.split(), n=1):
                target_name = name
                break
        if target_name:
            speak(f"{target_name} को कॉल लगा रहा हूँ बॉस...", "happy")
            os.system(f"termux-telephony-call {contacts[target_name]}")
            time.sleep(4)
            continue
        else:
            speak("किसे कॉल करना है बॉस? नाम बताइए।", "normal")
            time.sleep(2)
            continue

    if "whatsapp" in result and ("message" in result or "मैसेज" in result or "msg" in result):
        parts = result.split("message") if "message" in result else result.split("मैसेज")
        if len(parts) > 1:
            target_text = parts[1].strip().split()
            if len(target_text) >= 2:
                contact_name = target_text[0].lower()
                message_text = " ".join(target_text[1:])
                for name, number in contacts.items():
                    if name in contact_name or difflib.get_close_matches(name, [contact_name], n=1):
                        speak(f"{contact_name} को WhatsApp मैसेज भेज रहा हूँ।", "happy")
                        os.system(f'termux-open-url "whatsapp://send?phone={number}&text={message_text}"')
                        time.sleep(3)
                        break
            else:
                speak("ऐसे बोलें: WhatsApp message Rahul Hello", "normal")
        continue

    # ==========================================
    # 5. अन्य कमांड्स
    # ==========================================
    if "समय" in result or "time" in result:
        current_time = os.popen("date +'%I:%M %p'").read().strip()
        reply = f"अभी {current_time} बजे हैं।"
    elif "तारीख" in result or "date" in result:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        reply = f"आज की तारीख है {today}"
    elif "बैटरी" in result or "battery" in result:
        try:
            data = json.loads(os.popen("termux-battery-status").read())
            reply = f"फोन में {data.get('percentage')} प्रतिशत बैटरी बची है।"
        except:
            reply = "बैटरी की जानकारी नहीं मिल पाई।"
    elif "चुटकुला" in result or "joke" in result:
        reply = random.choice(jokes)
        emotion = "excited"

    if not reply:
        reply, emotion = smart_reply(result, brain)

    if not reply:
        reply = "माफ़ कीजिए बॉस, मैं समझ नहीं पाया। कृपया साफ़ बोलें।"
        emotion = "normal"

    if reply:
        speak(reply, emotion)
    
    time.sleep(1)
