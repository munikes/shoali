#    This Python file uses the following encoding: utf-8 .
#    See http://www.python.org/peps/pep-0263.html for details

#    Software as a service (SaaS), which allows anyone to manage their money,
#    in the virtual world, transparently, without intermediaries.
#
#    Copyright (C) 2013 Diego Pardilla Mata
#
#    This file is part of Shoali.
#
#    Shoali is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
logger = logging.getLogger(__name__)
from decimal import Decimal
from celery.task import task
from pymongo import MongoClient
import bitcoinrpc
from main.apps.core.utils import get_blocks, update_blocks, sum_balance,\
        get_block

@task
def get_balance_and_progress_status(bitcoin_address):
    """
    Get balance of a bitcoin address and the progress status of the task
    """
    #init variables
    blocks = []
    balance = 0
    update = False
    first_block = 225990
    number_blocks = 225991
    # get the total number of blocks in this moment
    # connect to bitcoin client
    con_btc = bitcoinrpc.connect_to_remote('mUniKeS', 'XXXXXXXXXXXXXXXXXXXX',
            host='agora-2', port=8332, use_https=False)
    try:
        logger.debug('Connection info: %s', con_btc.getinfo())
    except Exception:
        logger.exception('Connection to bitcoin client failed.')
        raise Exception ('Connection to bitcoin client failed.')
    # connect to database
    try:
        con_db = MongoClient('localhost', 27017)
        logger.debug('database connection: %s', con_db)
    except Exception as e:
        logger.exception(e)
        raise Exception (e)
    db = con_db['shoali']
    logger.debug('database name: %s', db)
    db_blocks = db['blocks']
    logger.debug('database collection: %s', db_blocks)
    # get the total number of blocks in this moment
    #number_blocks = con_btc.getblockcount()
    logger.debug('number of BTC blocks: %d', number_blocks)
    # select the database entry with this bitcoin address
    bitcoin_entry = db_blocks.find_one({'bitcoin_address':bitcoin_address})
    logger.debug('bitcoin MongoDB entry: %s', bitcoin_entry)
    # select the database entry with this bitcoin address
    if bitcoin_entry and bitcoin_entry.get('last_block') < number_blocks:
        # update bitcoin database entry
        first_block = bitcoin_entry.get('last_block') + 1
        update = True
    elif bitcoin_entry and bitcoin_entry.get('last_block') > number_blocks:
        logger.warning('The last block of %s is bigger than the number of\
 blocks in bitcoin network, entry will be deleted from the\
 database and will try again to put!', bitcoin_address)
        db_blocks.remove({'bitcoin_address':bitcoin_address})
    if not bitcoin_entry or bitcoin_entry.get('last_block') != number_blocks:
        # Caution with block 0, I DONT KNOW WHY GIVE AND EXCEPTION in transaction
        # info: InvalidAddressOrKey(No information available about transaction)
        if (first_block == 0 and
                bitcoin_address == '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'):
            blocks.append(0)
            first_block = 1
        elif first_block == 0:
            first_block = 1
        # do the loop
        for i in range (first_block, number_blocks + 1):
            get_balance_and_progress_status.update_state(state='PROGRESS',
                    meta={'first': first_block,'current': i,
                        'last': number_blocks})
            if get_block(con_btc, bitcoin_address, i):
                blocks.append(i)
        if update:
            bitcoin_entry['last_block'] = number_blocks
            bitcoin_entry['blocks'] += blocks
            bitcoin_entry['blocks'].sort()
            logger.info ('bitcoin entry: %s has been update', bitcoin_entry)
        else:
            bitcoin_entry = {'bitcoin_address':bitcoin_address, 'blocks':blocks,
                    'first_block':first_block, 'last_block':number_blocks}
            logger.info('blocks: %s', bitcoin_entry)
        balance = sum_balance(con_btc, bitcoin_entry)
        if isinstance(balance, Decimal):
            balance = float(balance)
        bitcoin_entry['balance'] = balance
    db_blocks.save(bitcoin_entry)
    return bitcoin_entry['balance']

@task
def get_balance(bitcoin_address):
    """
    Get balance of a bitcoin address
    """
    # init variables
    balance = 0
    update = False
    first_block = 225990
    number_blocks = 225991
    # connect to bitcoin client
    con_btc = bitcoinrpc.connect_to_remote('mUniKeS', 'XXXXXXXXXXXXXXXXXXXX',
            host='agora-2', port=8332, use_https=False)
    try:
        logger.debug('Connection info: %s', con_btc.getinfo())
    except Exception:
        logger.exception('Connection to bitcoin client failed.')
        raise Exception ('Connection to bitcoin client failed.')
    # connect to database
    try:
        con_db = MongoClient('localhost', 27017)
        logger.debug('database connection: %s', con_db)
    except Exception as e:
        logger.exception(e)
        raise Exception (e)
    db = con_db['shoali']
    logger.debug('database name: %s', db)
    blocks = db['blocks']
    logger.debug('database collection: %s', blocks)
    # get the total number of blocks in this moment
    #number_blocks = con_btc.getblockcount()
    logger.debug('number of BTC blocks: %d', number_blocks)
    # select the database entry with this bitcoin address
    bitcoin_entry = blocks.find_one({'bitcoin_address':bitcoin_address})
    logger.debug('bitcoin MongoDB entry: %s', bitcoin_entry)
    # select the database entry with this bitcoin address
    if bitcoin_entry and bitcoin_entry.get('last_block') < number_blocks:
        # update bitcoin database entry
        update = True
    elif bitcoin_entry and bitcoin_entry.get('last_block') > number_blocks:
        logger.warning('The last block of %s is bigger than the number of\
 blocks in bitcoin network, entry will be deleted from the\
 database and will try again to put!', bitcoin_address)
        blocks.remove({'bitcoin_address':bitcoin_address})
    if not bitcoin_entry or bitcoin_entry.get('last_block') != number_blocks:
        if update:
            bitcoin_entry = update_blocks(con_btc, bitcoin_entry, number_blocks)
        else:
            bitcoin_entry = get_blocks(con_btc, bitcoin_address, first_block,
                    number_blocks)
        balance = sum_balance(con_btc, bitcoin_entry)
        if isinstance(balance, Decimal):
            balance = float(balance)
        bitcoin_entry['balance'] = balance
    blocks.save(bitcoin_entry)
    return bitcoin_entry['balance']
