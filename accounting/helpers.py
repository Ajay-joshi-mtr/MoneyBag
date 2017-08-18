from .models import AccountHead as Head
from django.db.models import Q
from .models import Transaction,TransactionDetails
from django.db import IntegrityError,transaction
import random
import string
from calendar import monthrange
from pprint import pprint
from decimal import Decimal

'''
This file has all helper method that need by accounting module
'''

class AccHelper():
    '''
    This class has all helpter method that related to accounting
    operation.
    '''

    def create_all_basic_acc_heads(new_user):
        Head.objects.bulk_create([
            Head(user=new_user, parent_head_code=0, name="Branch / Divisions", type="ast", head_code=1, ledger_head_code=""),
            Head(user=new_user, parent_head_code=0, name="Capital Account", type="oe", head_code=2, ledger_head_code=""),
            Head(user=new_user, parent_head_code=0, name="Current Liabilities", type="lib", head_code=3, ledger_head_code=""),
            Head(user=new_user, parent_head_code=0, name="Current Assets", type="ast", head_code=4, ledger_head_code=""),
            Head(user=new_user, parent_head_code=0, name="Direct Expenses", type="exp", head_code=5, ledger_head_code=""),
            Head(user=new_user, parent_head_code=0, name="Direct Incomes", type="inc", head_code=6, ledger_head_code=""),
            Head(user=new_user, parent_head_code=0, name="Fixed Assets", type="ast", head_code=7, ledger_head_code=""),
            Head(user=new_user, parent_head_code=0, name="Indirect Expenses", type="exp", head_code=8, ledger_head_code=""),
            Head(user=new_user, parent_head_code=0, name="Indirect Incomes", type="inc", head_code=9, ledger_head_code=""),
            Head(user=new_user, parent_head_code=0, name="Investments", type="ast", head_code=10, ledger_head_code=""),
            Head(user=new_user, parent_head_code=0, name="Suspense A/c", type="ast", head_code=11, ledger_head_code=""),
            Head(user=new_user, parent_head_code=0, name="Loan Account", type="lib", head_code=12, ledger_head_code=""),
            Head(user=new_user, parent_head_code=4, name="Stock", type="ast", head_code=13, ledger_head_code=""),
            Head(user=new_user, parent_head_code=7, name="Property and Equipment", type="ast", head_code=14, ledger_head_code=""),
            Head(user=new_user, parent_head_code=3, name="Payables", type="lib", head_code=15, ledger_head_code=""),
            Head(user=new_user, parent_head_code=4, name="Receivables", type="ast", head_code=16, ledger_head_code=""),
            Head(user=new_user, parent_head_code=6, name="Service Revenue", type="inc", head_code=17, ledger_head_code=""),
            Head(user=new_user, parent_head_code=5, name="Service Expenditure", type="exp", head_code=18, ledger_head_code=""),
            Head(user=new_user, parent_head_code=4, name="Cash at Hand", type="ast", head_code=19, ledger_head_code=""),
            Head(user=new_user, parent_head_code=4, name="Banks", type="ast", head_code=20, ledger_head_code=""),
            Head(user=new_user, parent_head_code=19, name="Cash", type="ast", head_code=21, ledger_head_code=""),
            Head(user=new_user, parent_head_code=6, name="Sales Revenue", type="inc", head_code=22, ledger_head_code=""),
            Head(user=new_user, parent_head_code=5, name="Cost of Goods Sold", type="exp", head_code=23, ledger_head_code=""),
            Head(user=new_user, parent_head_code=4, name="Mobile Banking", type="ast", head_code=24, ledger_head_code=""),
            Head(user=new_user, parent_head_code=3, name="Vat account", type="lib", head_code=25, ledger_head_code=""),
            Head(user=new_user, parent_head_code=5, name="Sales Discount", type="exp", head_code=26, ledger_head_code=""),
            Head(user=new_user, parent_head_code=6, name="Income Statement Summary", type="inc", head_code=27, ledger_head_code=""),
            Head(user=new_user, parent_head_code=6, name="General Revenue", type="inc", head_code=28, ledger_head_code=""),
            Head(user=new_user, parent_head_code=5, name="General Expenditure", type="exp", head_code=29, ledger_head_code=""),
            Head(user=new_user, parent_head_code=17, name="Forbidden Adjustment", type="inc", head_code=30, ledger_head_code=""),
        ])

    def get_all_group_heads(user,head_types=None):
        if head_types:
            return Head.objects.filter(Q(user=user),Q(parent_head_code__in=head_types) | Q(head_code__in=head_types)).order_by('id')

        return Head.objects.filter(user=user).order_by('id')

    def get_certain_group_heads(user,head_types):
        return Head.objects.filter(user=user,head_code__in=head_types).order_by('id')

    def get_head_type(parent_head_code,user_id):
        parent_head = Head.objects.filter(head_code=parent_head_code,user=user_id).first()
        return parent_head.type

    def get_heads_tree(user,payments_only=None):
        #all_heads = Head.objects.filter(user=user).order_by('id')
        if payments_only:
            head_types = [AccConstant.ACC_HEAD_CASH, AccConstant.ACC_HEAD_BANK, AccConstant.ACC_HEAD_MOBILE_BANKING]
            all_heads = AccHelper.get_all_group_heads(user,head_types)
        else:
            all_heads = AccHelper.get_all_group_heads(user)

        heads_dict = dict()
        #sort heads according to parent using dictonary of list of dict
        for head in all_heads:
            head_dict = {'name': head.name, 'head_code': head.head_code, 'id': head.id, 'ledger_head_code': head.ledger_head_code}
            # print(head.parent_head_code,"=>",head_dict)
            if head.parent_head_code in heads_dict:
                heads_dict[head.parent_head_code].append(head_dict)
            else:
                heads_dict[head.parent_head_code] = [head_dict]

        tstring = ['']
        #call tree builder method
        AccHelper.create_tree(heads_dict,heads_dict[sorted(list(heads_dict.keys()))[0]],tstring)
        return  tstring

    #build head tree using recersive call from parent to child
    def create_tree(heads, parent,tstring):
        for l in parent:
            tstring[0] +='<li class="tree-menu-item-hover"><span><p>'+l['name']+'</p><button data-id="'+str(l['id'])+'" data-ledger-code="'+str(l['ledger_head_code'])+'" type="button" class="tree-menu-item btn bg-blue btn-circle waves-effect waves-circle waves-light waves-float pull-right btnEdit"  data-toggle="tooltip" data-placement="top" title="" data-original-title="Edit"><i class="material-icons">mode_edit</i></button></span></span></span>';
            if l['id'] in heads:
                tstring[0] +='<ul>'
                #call method itself for child heads
                AccHelper.create_tree(heads,heads[l['id']], tstring)
                tstring[0] += '</ul>'
                tstring[0] += '</li>'

    #form voucher validation
    def validate_voucher(data):
        payment_methods = data.getlist('payment_methods[]')
        if data.get('acc_head_id',False) and data.get('date',False) and len(payment_methods):
            return True
        return False
    #form acc voucher validation
    def validate_acc_voucher(data):
        if data.get('debit_head',False) and data.get('credit_head',False) and data.get('date',False) and data.get('amount'):
            return True
        return False

    #create random string
    def generate_random_string(length):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

    #create voucher
    def create_voucher(request,voucher_type):
       voucher_id = 0
       payment_methods = request.POST.getlist('payment_methods[]')
       payment_methods_amount = request.POST.getlist('payment_method_amount[]')
       payment_methods_note = request.POST.getlist('payment_method_note[]')

       with transaction.atomic():
           try:
               if voucher_type == AccConstant.VOUCHER_RECEIPT:
                   for index, item in enumerate(payment_methods):
                       note = None
                       if 0 <= index < len(payment_methods_note):
                           note = payment_methods_note[index]

                       trans_id = AccHelper.create_new_transaction(
                           request.user.id,
                           None,
                           request.POST.get('date'),
                           voucher_type,
                           note
                       )
                       AccHelper.create_transaction_details(
                           trans_id,
                           payment_methods[index],
                           AccConstant.DEBIT,
                           payment_methods_amount[index]
                       )
                       AccHelper.create_transaction_details(
                           trans_id,
                           request.POST.get('acc_head_id'),
                           AccConstant.CREDIT,
                           payment_methods_amount[index]
                       )
                       voucher_id = trans_id
               elif voucher_type == AccConstant.VOUCHER_PAYMENT:
                   for index, item in enumerate(payment_methods):
                       note = None
                       if 0 <= index < len(payment_methods_note):
                           note = payment_methods_note[index]

                       trans_id = AccHelper.create_new_transaction(
                           request.user.id,
                           None,
                           request.POST.get('date'),
                           voucher_type,
                           note
                       )
                       AccHelper.create_transaction_details(
                           trans_id,
                           payment_methods[index],
                           AccConstant.CREDIT,
                           payment_methods_amount[index]
                       )
                       AccHelper.create_transaction_details(
                           trans_id,
                           request.POST.get('acc_head_id'),
                           AccConstant.DEBIT,
                           payment_methods_amount[index]
                       )
                       voucher_id = trans_id
           except IntegrityError:
               return False

       return voucher_id


    #create account transaction
    def create_new_transaction(user_id, ref_id, date, voucher_type, description):
        new_tran = Transaction()
        new_tran.user_id = user_id
        if ref_id is not None:
         new_tran.transaction_ref_id = ref_id
        new_tran.transaction_date = date
        new_tran.voucher_type = voucher_type
        new_tran.voucher_number = AccHelper.generate_random_string(8)
        new_tran.voucher_status = AccConstant.VOUCHER_STATUS_PROCESSED
        if description is not None:
            new_tran.description = description
        new_tran.save()

        return new_tran.id

    #create account transaction details
    def create_transaction_details(tran_id,account_head,position,amount):
        details = TransactionDetails()
        details.transaction_id = tran_id
        details.account_head_id = account_head
        details.position = position
        details.amount = amount
        details.save()

        return True

    #get child heads
    def get_all_child_heads(user):
        parent_heads = Head.objects.filter(user=user).values_list('parent_head_code',flat=True).distinct()
        child_heads = Head.objects.filter(Q(user=user),~Q(parent_head_code=0),~Q(id__in=parent_heads),~Q(head_code__in=parent_heads)).order_by('name').values_list('id','name')
        return child_heads

    #get voucher full name
    def get_voucher_type_name(type):
        return {
            AccConstant.VOUCHER_PAYMENT : 'Payment Voucher',
            AccConstant.VOUCHER_RECEIPT : 'Receipt Voucher',
            AccConstant.VOUCHER_CONTRA : 'Contra Voucher',
            AccConstant.VOUCHER_JOURNAL : 'Journal Voucher',
            AccConstant.VOUCHER_DEBIT_NOTE : 'Debit Note',
            AccConstant.VOUCHER_CREDIT_NOTE : 'Credit Note',
            AccConstant.VOUCHER_VAT : 'Vat Challan',
            AccConstant.VOUCHER_DISCOUNT : 'Discount Voucher',
        }[type]

    #detect account type
    def detect_account_type(account):
        return {
            'oe' : 'cr',
            'ast' : 'dr',
            'lib' : 'cr',
            'inc' : 'cr',
            'exp' : 'dr',
        }[account]

    #generate income statements
    def generate_income_statement(user,month_year):
        #get all the receipts
        receipts = Head.objects.filter(user=user,parent_head_code=0,type=AccConstant.INCOME)
        income_statement_content = [{
            'title': '<b>Revenues</b>',
            'amount_column_1': '',
            'amount_column_2': ''
        }]
        income = [0]
        for recipt in receipts:
            AccHelper.develop_childs_statement(user,recipt,income_statement_content,month_year,AccConstant.INCOME,0,income)

        income_statement_content.append(
            {
                'title': '',
                'amount_column_1': '',
                'amount_column_2': format(income[0], '.2f')
            }
        )
        income_statement_content.append(
            {
                'title': '',
                'amount_column_1': '',
                'amount_column_2': ''

            }
        )
        # get all the payments
        income_statement_content.append(
            {
                'title': '<b>Expenses</b>',
                'amount_column_1': '',
                'amount_column_2': ''

            }
        )
        # get all the receipts
        receipts = Head.objects.filter(user=user, parent_head_code=0, type=AccConstant.EXPENSE)
        expense = [0]
        for recipt in receipts:
            AccHelper.develop_childs_statement(user, recipt, income_statement_content, month_year, AccConstant.EXPENSE, 0, expense)

        income_statement_content.append(
            {
                'title': '',
                'amount_column_1': '',
                'amount_column_2': format(expense[0], '.2f')

            }
        )
        income_statement_content.append(
            {
                'title': '',
                'amount_column_1': '',
                'amount_column_2': ''

            }
        )
        net_income = income[0] - expense[0]
        if net_income >= 0:
            income_statement_content.append(
                {
                    'title': '<b>Net Income</b>',
                    'amount_column_1': '',
                    'amount_column_2': '<b>'+str(format(net_income, '.2f'))+'<b>'

                }
            )
        else:
            income_statement_content.append(
                {
                    'title': '<b>Net Loss</b>',
                    'amount_column_1': '',
                    'amount_column_2': '<b>' + str(abs(net_income)) + '<b>'

                }
            )
        return income_statement_content

    #get child heads statement
    def develop_childs_statement(user,head_info,income_statement_content,month_year,st_type,level,summation):
        child_heads = Head.objects.filter(user=user,parent_head_code=head_info.head_code).count()
        if child_heads:
            #get childs
            receipts = Head.objects.filter(user=user, parent_head_code=head_info.head_code)
            spaces =""
            for x in range(0,level):
                spaces = spaces + '&nbsp;&nbsp;&nbsp;'

                income_statement_content.append(
                {
                    'title': spaces+head_info.name+':',
                    'amount_column_1': '',
                    'amount_column_2': ''

                }
                )

            level = level + 1
            for receipt in receipts:
                AccHelper.develop_childs_statement(user,receipt,income_statement_content,month_year,st_type,level,summation)

        else:
            total = Decimal(0.00)
            #head has no child so lets search its transation total
            #get request month last day
            month_year_part = month_year.split('-')
            last_day = monthrange(int(month_year_part[0]),int(month_year_part[1]))
            date_q = month_year+'-'+str(last_day[1])

            #get unique transactions
            unique_transactions = TransactionDetails.objects.select_related('transaction').filter(
                Q(transaction__transaction_date__lte=date_q),
                Q(account_head_id=head_info.id)
            ).values_list('transaction_id',flat=True)

            #get transactions
            transactions = TransactionDetails.objects.select_related('transaction').filter(
                Q(transaction_id__in=unique_transactions),
                ~Q(account_head_id=head_info.id)
            )

            for transaction in transactions:
                if AccHelper.detect_account_type(st_type) == AccConstant.DEBIT:
                    if transaction.position == AccConstant.DEBIT:
                        total = total - transaction.amount
                    else:
                        total = total + transaction.amount
                else:
                    if transaction.position == AccConstant.CREDIT:
                        total = total - transaction.amount
                    else:
                        total = total + transaction.amount

            summation[0] = summation[0] + total
            spaces = ""
            for x in range(0, level):
                spaces = spaces + '&nbsp;&nbsp;&nbsp;'

            income_statement_content.append(
                {
                    'title': spaces + head_info.name + ':',
                    'amount_column_1': total,
                    'amount_column_2': ''

                }
            )

    #get heads except parents
    def get_heads(user):
        #get all distinct parent heads
        parent_heads = Head.objects.filter(user=user).distinct().values_list('parent_head_code',flat=True)
        p_heads = []
        for head in parent_heads:
            p_heads.append(head)
        #get all kids heads
        kids_heads = Head.objects.filter(Q(user=user),~Q(parent_head_code=0),~Q(id__in=p_heads),~Q(head_code__in=p_heads)).order_by('name').values('id','name')
        return kids_heads

    #generate ledger statement
    def generate_ledger_statement(user,head_id,month_year):
        # get request month last day
        month_year_part = month_year.split('-')
        last_day = monthrange(int(month_year_part[0]), int(month_year_part[1]))
        date_q = month_year + '-' + str(last_day[1])

        # get unique transactions
        unique_transactions = TransactionDetails.objects.select_related('transaction').filter(
            Q(transaction__transaction_date__lte=date_q),
            Q(account_head_id=head_id)
        ).values_list('transaction_id', flat=True)

        # get transactions
        transactions = TransactionDetails.objects.select_related('transaction').filter(
            Q(transaction_id__in=unique_transactions),
            ~Q(account_head_id=head_id)
        ).select_related('account_head').order_by('-transaction__transaction_date')

        head = Head.objects.filter(id=head_id).first()
        total = 0
        ledger_content = []
        for transaction in transactions:
            dr_amount = ''
            cr_amount = ''
            if AccHelper.detect_account_type(head.type) == AccConstant.DEBIT:
                if transaction.position == AccConstant.DEBIT:
                    total = total - transaction.amount
                    dr_amount = transaction.amount
                else:
                    total = total + transaction.amount
                    cr_amount = transaction.amount
            else:
                if transaction.position == AccConstant.CREDIT:
                    total = total - transaction.amount
                    cr_amount = transaction.amount
                else:
                    total = total + transaction.amount
                    dr_amount = transaction.amount

            ledger_content.append(
                {
                    'transection_id' : transaction.transaction.id,
                    'date' : transaction.transaction.transaction_date,
                    'title' : transaction.account_head.name+'('+str(transaction.account_head.head_code)+')',
                    'voucher' : transaction.transaction.voucher_number,
                    'dr_amount' : dr_amount,
                    'cr_amount' : cr_amount,
                    'balance' : total
                }
            )

        return ledger_content


class AccConstant():
    '''
    This class is a static value container
    '''

    ASSET = "ast"
    LIABILITY = "lib"
    OWNERS_EQUITY = "oe"
    EXPENSE = "exp"
    INCOME = "inc"
    DEBIT = "dr"
    CREDIT = "cr"

    VOUCHER_INVOICE_SALES = 1
    VOUCHER_INVOICE_PURCHASE = 2
    VOUCHER_INVOICE_EXPENSE = 5

    VOUCHER_JOURNAL = 3
    VOUCHER_CONTRA = 4
    VOUCHER_PAYMENT = 5
    VOUCHER_RECEIPT = 6

    VOUCHER_DEBIT_NOTE = 7
    VOUCHER_CREDIT_NOTE = 8

    VOUCHER_VAT = 9
    VOUCHER_DISCOUNT = 10

    VOUCHER_STATUS_ENTERED = 1
    VOUCHER_STATUS_UNDER_PROCESS = 2
    VOUCHER_STATUS_PROCESSED = 3
    VOUCHER_STATUS_INACTIVE = 0


    ACC_HEAD_LOAN = 12
    ACC_HEAD_STOCK = 13
    ACC_HEAD_PAYABLE = 15
    ACC_HEAD_RECEIVABLE = 16
    ACC_HEAD_CASH = 19
    ACC_HEAD_BANK = 20
    ACC_HEAD_MOBILE_BANKING = 24
    ACC_HEAD_VAT_ACCOUNT = 25
    ACC_HEAD_SALES_DISCOUNT = 26
    ACC_HEAD_SALES_REVENUE = 22
    ACC_HEAD_SERVICE_REVENUE = 17
    ACC_HEAD_SERVICE_EXPENDITURE = 18
    ACC_HEAD_COGS = 23
    ACC_HEAD_CAPITAL = 2
    ACC_HEAD_DIRECT_EXPENSES = 5
    ACC_HEAD_DIRECT_INCOMES = 6
    ACC_HEAD_INCOME_SUMMARY = 27
    ACC_HEAD_FORBIDDEN_ADJUSTMENT = 30
    ACC_HEAD_GENERAL_REVENUE = 28
    ACC_HEAD_GENERAL_EXPENDITURE = 29

    ACTIVE = 1
    DISABLE = 0

    SERVICE_EXPENDITURE = 18
    SERVICE_REVENUE = 17

