from abc import abstractproperty
from threading import local
from sqlalchemy import exc
from sqlalchemy.exc import DataError
import telebot, time, sqlite3, datetime
from sqlalchemy import create_engine
from time import sleep
import sqlalchemy
import app_logger

logger = app_logger.get_logger(__name__)

try:
    bot = telebot.TeleBot('<TELEGRAM BOT TOKEN>')
    dbname = '<DBNAME>'
    user = '<USER>'
    password = '<PASSWORD>'
    host = "<HOST IP>"
    port = "<PORT>"
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
    local_engine = create_engine('sqlite:////root/botCopart/bot.db')

    #for all aucs
    data = engine.execute('SELECT count(*) FROM cars').fetchall()
    local_engine.execute(f'INSERT INTO records (record) VALUES ({data[0][0]})')
    id = local_engine.execute('SELECT id FROM records ORDER BY id DESC LIMIT 1')
    previous = local_engine.execute(f'SELECT record FROM records WHERE id={id.fetchall()[0][0]-1}').fetchall()

    bot.send_message(<TELEGRAM CHAT ID>, f'Всего: {data[0][0]}, всего добавлено за сутки: {int(data[0][0])-int(previous[0][0])}')

    total = data[0][0]

    #for iaai
    data = engine.execute("SELECT count(*) FROM cars WHERE auc_name='iaai'").fetchall()
    local_engine.execute(f'INSERT INTO records_iaai (record) VALUES ({data[0][0]})')
    id = local_engine.execute('SELECT id FROM records_iaai ORDER BY id DESC LIMIT 1')
    previous = local_engine.execute(f'SELECT record FROM records_iaai WHERE id={id.fetchall()[0][0]-1}').fetchall()
    bot.send_message(<TELEGRAM CHAT ID>, f'Добавлено за сутки iaai: {int(data[0][0])-int(previous[0][0])}')

    #for other
    now = local_engine.execute(f'INSERT INTO records_copart (record) VALUES ({int(total)-int(data[0][0])})')
    id = local_engine.execute('SELECT id FROM records_copart ORDER BY id DESC LIMIT 1')
    previous = local_engine.execute(f'SELECT record FROM records_copart WHERE id={id.fetchall()[0][0]-1}').fetchall()
    bot.send_message(<TELEGRAM CHAT ID>, f'Добавлено за сутки copart: {int(total)-data[0][0]-int(previous[0][0])}')

    #for aucs nums
    final = engine.execute(f"SELECT DISTINCT name FROM aucs WHERE date >= NOW() - INTERVAL '24 HOURS'").fetchall()
    bot.send_message(<TELEGRAM CHAT ID>, f'Количество аукционов за сутки: {len(final)}')

except Exception as ex:
    logger.error(str(ex))

