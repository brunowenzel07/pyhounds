import sys
import time
import telepot
import telepot.namedtuple
from telepot.loop import MessageLoop
import predict
import Queue
import threading 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Normalizer
from database import Database

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    m = telepot.namedtuple.Message(**msg)

    db = Database("data/data_train.csv")
    db2 = Database("predicts/predicts.csv")
    data_train = db.load()
    data_test = db.load_tuning()
    scaler = Normalizer()
    X_scaler = scaler.fit_transform(data_train[0])
    clf = KNeighborsClassifier(n_neighbors=2, p=3)
    clf.fit(X_scaler, data_train[1])
    
    if content_type == 'text':
        
        url  = msg["text"]

        bot.sendMessage(chat_id, "Aguarde... Iniciando processamento de dados")
        stats = predict.run(url)
        bot.sendMessage(chat_id, "Processamento finalizado... Insira o número dos galgos")

        traps = 
        
        for i, s in enumerate(stats):
        for k, t in enumerate(stats):
            try: 
                a_position = int(s[-1])
                b_position = int(t[-1])
                if a_position != b_position:                    
                    if a_position == a and b_position == b:                        
                        row = s[:-1] + t[:-1]
                        pred = clf.predict(scaler.fit_transform([row]))
                        score = clf.predict_proba(scaler.fit_transform([row]))
                        
                        if int(pred) == 0:
                            label = "%sv%s" % (a, b)
                        else:
                            label = "%sv%s" % (b, a)
                        
            except Exception as a:
                pass

        bot.sendMessage(chat_id, label)


TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print 'Listening ...'

# Keep the program running.
while 1:
    time.sleep(10)