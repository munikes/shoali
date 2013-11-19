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
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from main.apps.core.models import BitcoinAddress, Loan
from main.apps.core.forms import BitcoinAddressForm, LoanForm
from main.apps.core.tasks import get_balance_and_progress_status

def begin (request):
    return render_to_response('index.html',{})

@login_required
def user_info (request):
    return render_to_response('user/main.html',{},
            context_instance=RequestContext(request))

@login_required
def user_btc_addresses (request):
    # init bitcoin address form
    form_btc = BitcoinAddressForm ()
    if request.method == 'POST':
        form_btc = BitcoinAddressForm (request.POST)
        if request.POST.get('add'):
            if form_btc.is_valid():
                # insert BTC address
                # see if exists
                bitcoin_address = form_btc.cleaned_data['bitcoin_address']
                if not BitcoinAddress.objects.filter(
                        bitcoin_address=bitcoin_address):
                    btc = form_btc.save(commit=False)
                    btc.save()
                    btc.users.add(request.user.id)
                elif BitcoinAddress.objects.filter(
                        bitcoin_address=bitcoin_address):
                    btc = BitcoinAddress.objects.get(
                            bitcoin_address=bitcoin_address)
                    btc.users.add(request.user.id)
                logger.debug('insert BTC address: %s', bitcoin_address)
        elif request.POST.get('delete'):
            try:
                btc = BitcoinAddress.objects.get(
                    bitcoin_address=request.POST.get('bitcoin_address'))
                btc.users.remove(request.user.id)
                if not btc.users.all():
                    btc.delete()
                logger.debug('delete BTC address: %s for user: %s',
                    bitcoin_address, request.user.id)
            except BitcoinAddress.DoesNotExist:
                logger.debug('not delete BTC address because this BTC: %s not \
exists for this user: %s', request.POST.get('bitcoin_address'), request.user.id)
        return render_to_response('user/main.html',{'form_btc':form_btc},
                context_instance=RequestContext(request))
    return render_to_response('user/main.html',
            {'form_btc':form_btc},context_instance=RequestContext(request))

@login_required
def lend_money(request):
    # init supply form
    form_loan = LoanForm()
    if request.method == 'POST':
        form_loan = LoanForm(request.POST)
        if request.POST.get('add'):
            if form_loan.is_valid():
                # insert the loan
                loan = form_loan.save(commit=False)
                loan.save()
                loan.lenders.add(request.user.id)
                logger.debug(form_loan)
                logger.debug('Create amount: %s %s - repayment period: %s %s - \
borrowers:%s and lenders:%s - interest: %s %%' % (loan.amount,
                    loan.get_unit_display(), loan.period,
                    loan.get_days_display(), loan.borrowers.all(),
                    loan.lenders.all(), loan.interest))
                return render_to_response('user/main.html',{'form_loan': form_loan},
                    context_instance=RequestContext(request))
        elif request.POST.get('delete'):
            loan_list = Loan.objects.filter(id__in=request.POST.getlist('loan'))
            for loan in loan_list:
                logger.debug('Delete amount: %s %s - repayment period: %s %s - \
borrowers:%s and lenders:%s - interest: %s %%' % (loan.amount,
                    loan.get_unit_display(), loan.period,
                    loan.get_days_display(), loan.borrowers.all(),
                    loan.lenders.all(), loan.interest))
            loan_list.delete()
        return  render_to_response('user/main.html', {'form_loan': form_loan},
            context_instance=RequestContext(request))
    return  render_to_response('user/main.html', {'form_loan': form_loan},
        context_instance=RequestContext(request))

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
        logger.debug("Celery task ID: %s", data)
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
            logger.debug("Celery task ID: %s", task_id)
            task = get_balance_and_progress_status.AsyncResult(task_id)
            data = {'result':task.result, 'state':task.state}
            logger.debug("Celery task result: %s", data)
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'
    return HttpResponse(json.dumps(data), mimetype='application/json')
