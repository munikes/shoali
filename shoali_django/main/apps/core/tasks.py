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
from celery.task import task
from pymongo import Connection
import bitcoinrpc
from main.apps.core.utils import get_blocks, update_blocks, sum_balance

@task
def get_balance(bitcoin_address):
    """
    Get balance of a bitcoin address
    """
    # connect to bitcoin client
    con_btc = bitcoinrpc.connect_to_remote('mUniKeS', 'XXXXXXXXXXXXXXXXXXXX',
            host='agora-2', port=8332, use_https=False)
    try:
        logging.debug('Connection info: %s', con_btc.getinfo())
    except Exception:
        logging.exception('Connection to bitcoin client failed.')
        raise Exception ('Connection to bitcoin client failed.')
    # connect to database
    try:
        con_db = Connection('localhost', 27017)
        logging.debug('database connection: %s', con_db)
    except Exception as e:
        logging.exception(e)
        raise Exception (e)
    db = con_db['shoali']
    logging.debug('database name: %s', db)
    blocks = db['blocks']
    logging.debug('database collection: %s', blocks)
    # get the total number of blocks in this moment
    #number_blocks = con_btc.getblockcount()
    number_blocks = 225999
    first_block = 225980
    logging.debug('number of BTC blocks: %d', number_blocks)
    # select the database entry with this bitcoin address
    bitcoin_entry = blocks.find_one({'bitcoin_address':bitcoin_address})
    logging.debug('bitcoin MongoDB entry: %s', bitcoin_entry)
    # select the database entry with this bitcoin address
    if bitcoin_entry and bitcoin_entry.get('last_block') < number_blocks:
        # update bitcoin database entry
        bitcoin_entry = update_blocks(con_btc, bitcoin_entry, number_blocks)
    elif bitcoin_entry and bitcoin_entry.get('last_block') > number_blocks:
        logging.warning('The last block of %s is bigger than the number of\
                blocks in bitcoin network, entry will be deleted from the\
                database and will try again to put!', bitcoin_address)
        blocks.remove({'bitcoin_address':bitcoin_address})
        bitcoin_entry = get_blocks(con_btc, bitcoin_address, first_block, number_blocks)
    elif not bitcoin_entry:
        bitcoin_entry = get_blocks(con_btc, bitcoin_address, first_block, number_blocks)
    blocks.save(bitcoin_entry)
    return sum_balance(con_btc, bitcoin_entry)
