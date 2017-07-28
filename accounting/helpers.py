from .models import AccountHead as Head

'''
This class has all helper method that need by accounting module
'''

class AccHelper():

    def create_all_basic_acc_heads(new_user):
        Head.objects.bulk_create([
            Head(user=new_user, name="Branch / Divisions", type="ast", head_code=1, ledger_head_code=""),
            Head(user=new_user, name="Capital Account", type="oe", head_code=2, ledger_head_code=""),
            Head(user=new_user, name="Current Liabilities", type="lib", head_code=3, ledger_head_code=""),
            Head(user=new_user, name="Current Assets", type="ast", head_code=4, ledger_head_code=""),
            Head(user=new_user, name="Direct Expenses", type="exp", head_code=5, ledger_head_code=""),
            Head(user=new_user, name="Direct Incomes", type="inc", head_code=6, ledger_head_code=""),
            Head(user=new_user, name="Fixed Assets", type="ast", head_code=7, ledger_head_code=""),
            Head(user=new_user, name="Indirect Expenses", type="exp", head_code=8, ledger_head_code=""),
            Head(user=new_user, name="Indirect Incomes", type="inc", head_code=9, ledger_head_code=""),
            Head(user=new_user, name="Investments", type="ast", head_code=10, ledger_head_code=""),
            Head(user=new_user, name="Suspense A/c", type="ast", head_code=11, ledger_head_code=""),
            Head(user=new_user, name="Loan Account", type="lib", head_code=12, ledger_head_code=""),
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

    def get_all_group_heads(user):
        return Head.objects.filter(user=user).values_list('head_code','name')
    def get_head_type(parent_head_code,user_id):
        parent_head = Head.objects.filter(head_code=parent_head_code,user=user_id).first()
        return parent_head.type


class AccConstant():

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
    ACC_HEAD_COGS = 23
    ACC_HEAD_CAPITAL = 2
    ACC_HEAD_DIRECT_EXPENSES = 5
    ACC_HEAD_INCOME_SUMMARY = 27
    ACC_HEAD_FORBIDDEN_ADJUSTMENT = 30
    ACC_HEAD_GENERAL_REVENUE = 28
    ACC_HEAD_GENERAL_EXPENDITURE = 29

    ACTIVE = 1
    DISABLE = 0

    SERVICE_EXPENDITURE = 18
    SERVICE_REVENUE = 17

