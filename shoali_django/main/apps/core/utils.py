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

import re
import socket
import logging

def unit_to_bytes(value):
    """
    Give a value with a metric (TB|GB|KB|MB) and returns the number of bytes
    p.e (1G|1GB|1 G|1 GB)
    """
    regex = re.compile('(^\d+[.|,]?\d*)\s?([T|G|M|K]?B?)$')
    if bool(regex.search(value)):
        digit = float(regex.match(value).group(1).replace(',','.'))
        metric = regex.match(value).group(2).replace('B','')
        digit = {'T':digit*1024**4, 'G':digit*1024**3,'M':digit*1024**2,\
                'K':digit*1024,'':digit}.get(metric)
        logging.info('digit: %s', digit)
        return digit
    else:
        logging.exception('Value have bad format')
        raise Exception ('Value have bad format.')

def get_blocks(connection, bitcoin_address, first_block, last_block):
    """
    Give a bitcoin address, connection to bitcoin client, fisrt and last block,
    and returns heights of all blocks involved with this bitcoin address in
    this interval of blocks
    p.e returns {'bitcoin_address':'1111', 'blocks':[0,1], 'first_block':0,
    'last_block':1}
    """
    blocks = []
    # Caution with block 0, I DONT KNOW WHY GIVE AND EXCEPTION in transaction
    # info: InvalidAddressOrKey(No information available about transaction)
    if (first_block == 0 and
            bitcoin_address == '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'):
        blocks.append(0)
        first_block = 1
    elif first_block == 0:
        first_block = 1
    for i in range (first_block, last_block + 1):
        # get block info
        while True:
            try:
                block = connection.getblock(connection.getblockhash(i))
            except socket.timeout:
                continue
            except Exception as e:
                logging.exception(e)
                raise Exception (e)
            break
        # get block transacctions
        for j in block.get('tx'):
            logging.debug('tx: %s', j)
            while True:
                try:
                    tx = connection.getrawtransaction(j)
                except socket.timeout:
                    continue
                except Exception as e:
                    logging.exception(e)
                    raise Exception (e)
                break
            for k in range(0, len(tx.vout)):
                for l in tx.vout[k].get('scriptPubKey').get('addresses'):
                    logging.debug('btc_addr: %s', l)
                    if l == bitcoin_address:
                        blocks.append(i)
                        break
                else:
                    continue
                break
            else:
                continue
            break
    btc_dict = {'bitcoin_address':bitcoin_address, 'blocks':blocks,
            'first_block':first_block, 'last_block':last_block}
    logging.info('blocks: %s', btc_dict)
    return btc_dict

def update_blocks(connection, bitcoin_entry, last_block):
    """
    Give a connection to bitcoin client, last block, and a
    bitcoin dictionary like {'bitcoin_address':'1111', 'blocks':[0,1],
    'first_block':0, 'last_block':1}, and update the bitcoin dictionary
    """
    bitcoin_address = bitcoin_entry.get('bitcoin_address')
    if bitcoin_entry.get('last_block') < last_block:
        update_block = get_blocks(connection, bitcoin_address,
                bitcoin_entry.get('last_block') + 1, last_block)
        bitcoin_entry['last_block'] = last_block
        bitcoin_entry['blocks'] += update_block['blocks']
        bitcoin_entry['blocks'].sort()
        logging.info ('bitcoin entry: %s has been update', bitcoin_entry)
    return bitcoin_entry

def sum_balance(connection, bitcoin_entry):
    """
    Give a connection to bitcoin client and bitcoin dictionary
    like {'bitcoin_address':'1111', 'blocks':[0,1],'first_block':0,
    'last_block':1}, and returns the balance of this bitcoin address
    """
    balance = 0
    bitcoin_address = bitcoin_entry.get('bitcoin_address')
    logging.debug ('bitcoin address: %s', bitcoin_address)
    blocks = bitcoin_entry.get('blocks')
    logging.debug ('blocks: %s', blocks)
    # Caution with block 0, I DONT KNOW WHY GIVE AND EXCEPTION in transaction
    # info: InvalidAddressOrKey(No information available about transaction)
    if bitcoin_address == '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa':
        balance = 50
        blocks = blocks[1:]
    for i in blocks:
        # get block info
        while True:
            try:
                block = connection.getblock(connection.getblockhash(i))
            except socket.timeout:
                continue
            except Exception as e:
                logging.exception(e)
                raise Exception (e)
            break
        # get block transacctions
        for j in block.get('tx'):
            logging.debug('tx: %s', j)
            while True:
                try:
                    tx = connection.getrawtransaction(j)
                except socket.timeout:
                    continue
                except Exception as e:
                    logging.exception(e)
                    raise Exception (e)
                break
            for k in range(0, len(tx.vout)):
                for l in tx.vout[k].get('scriptPubKey').get('addresses'):
                    logging.debug('btc_addr: %s', l)
                    if l == bitcoin_address:
                        balance = balance +\
                                  connection.gettxout(j, k).value
                        logging.debug('balance: %s', balance)
                        break
                else:
                    continue
                break
            else:
                continue
            break
    logging.info('Total balance: %s', balance)
    return balance
