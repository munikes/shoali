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
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson as json

from main.apps.core.forms import BitcoinAddressForm
from main.apps.core.tasks import get_balance_and_progress_status

def begin (request):
    return render_to_response('index.html',{})

def getbalance (request):
    """
    Get balance of a bitcoin address
    """
    # init variables
    form_btc = BitcoinAddressForm()
    data = ''
    if request.is_ajax():
        job = get_balance_and_progress_status.delay(
                request.POST.get('bitcoin_address'))
        data = job.id
        logging.debug("Celery task ID: %s", data)
        json_data = json.dumps(data)
        return HttpResponse(json_data, mimetype='application/json')
    else:
        return render_to_response ('query.html', {'form_btc': form_btc},
            context_instance = RequestContext(request))

def update_task(request):
    """
    A view to report the progress of the task
    """
    # init variables
    data = ''
    if request.is_ajax():
        if 'task' in request.POST.keys() and request.POST['task']:
            task_id = request.POST['task']
            logging.debug("Celery task ID: %s", task_id)
            task = get_balance_and_progress_status.AsyncResult(task_id)
            data = {'result':task.result, 'state':task.state}
            logging.debug("Celery task result: %s", data)
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'
    return HttpResponse(json.dumps(data), mimetype='application/json')
