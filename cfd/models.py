import logging
import calendar
from datetime import *
from dateutil.relativedelta import *

from django.db import models
from django.contrib.auth import get_user_model

import reversion

from cfd.fields import MultiSelectField
from cfd.managers import HistoryManager

User = get_user_model()

# Create your models here.
class client(models.Model):
    #define fields
    #format is [database_column_name] = models.[FiedlType]('[Display Name]',[options])
    CLIENT_NAME	= models.CharField('Client Name',max_length=255)

    def __str__(self):
        return self.CLIENT_NAME

@reversion.register()
class cfd(models.Model):
    class Meta:
            verbose_name = 'Client Financial Record'
            verbose_name_plural = 'Client Financial Records'
            #ordering = ('self.client.CLIENT_NAME',)

    #define drop down values
    #An iterable (e.g., a list or tuple) consisting itself of iterables of exactly two items (e.g. [(A, B), (A, B) ...]) to use as choices for this field. If choices are given, they’re enforced by model validation and the default form widget will be a select box with these choices instead of the standard text field.
#The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name. For example:

    DROP_DOWN_MENU_21_CHOICES = (
        ('Y','Y'),
        ('N','N'),
        ('TBD','TBD')
    )
    
    DROP_DOWN_MENU_23_CHOICES = (
        ('Y - Retail-90','Y - Retail-90'),
        ('Y - Retail at Mail Rates','Y - Retail at Mail Rates'),
        ('Y - Retail-90 & Retail at Mail Rates','Y - Retail-90 & Retail at Mail Rates'),
        ('N','N')
    )

    DROP_DOWN_MENU_24_CHOICES = (
        ('Include - Explicit in Contract','Include - Explicit in Contract'),
        ('Include - Assumed by CE','Include - Assumed by CE'),
        ('Exclude - Explicit in Contract','Exclude - Explicit in Contract'),
        ('Exclude - Assumed by CE','Exclude - Assumed by CE'),
        ('TBD','TBD')
    )

    DROP_DOWN_MENU_25_CHOICES = (
        ('Include in GER - Explicit in Contract','Include in GER - Explicit in Contract'),
        ('Include in GER - Assumed by CE','Include in GER - Assumed by CE'),
        ('Include in BER - Explicit in Contract','Include in BER - Explicit in Contract'),
        ('Include in BER - Assumed by CE','Include in BER - Assumed by CE'),
        ('Exclude - Explicit in Contract','Exclude - Explicit in Contract'),
        ('Exclude - Assumed by CE','Exclude - Assumed by CE'),
        ('TBD','TBD')
    )
    
    DROP_DOWN_MENU_41 = (
        ('Transplant','Transplant'),
        ('Hepatitis B','Hepatitis B'),
        ('CMV Agents','CMV Agents'),
        ('HIV','HIV'),
        ('Anticoagulants','Anticoagulants'),
        ('Hepatitis C','Hepatitis C'),
        ('PCSK9','PCSK9'),
        ('TBD','TBD')
        )
    
    DROP_DOWN_MENU_CONTRACT_TYPE_CHOICES = (
        ('Baseline Remedy','Baseline Remedy'),
        ('Previous PBM Contract','Previous PBM Contract'),
        ('Standard','Standard'),
        ('TBD','TBD')
    )
    
    DROP_DOWN_MENU_42 = (
        ('Per Brand','Per Brand'),
        ('Per Rx','Per Rx'),
        ('TBD','TBD')
    )
    
    default_contract_start_date = date.today()
    default_contract_end_date = default_contract_start_date+relativedelta(years=+1)
    
    #define fields
    #format is [database_column_name] = models.[FiedlType]('[Display Name]',[options])
    #CLIENT_NAME = models.CharField('Client Name',max_length=255)
    CLIENT = models.ForeignKey(
                                client,
                                on_delete=models.PROTECT)
    CONTRACT_DESCRIPTION = models.TextField('Contract Description',max_length=500,blank=True)
    CONTRACT_TYPE = models.CharField('Contract Type',max_length=25,choices=DROP_DOWN_MENU_CONTRACT_TYPE_CHOICES)
    START_DATE = models.DateField('Contract Start Date',default=default_contract_start_date)
    END_DATE = models.DateField('Contract End Date',default=default_contract_end_date)
    GUAR_BM_EZBD_DCT = models.DecimalField('Mail Brand AWP Discount (excluding ZBDs)',max_digits=6, decimal_places=3, default=0)
    #GUAR_BM_EZBD_DCT = models.PercentField('Mail Brand AWP Discount (excluding ZBDs)')
    GUAR_BM_IZBD_DCT = models.DecimalField('Mail Brand AWP Discount (including ZBDs)',max_digits=6, decimal_places=3, default=0)
    GUAR_BR_EZBD_DCT = models.DecimalField('Retail Brand AWP Discount (excluding ZBDs)',max_digits=6, decimal_places=3, default=0)
    GUAR_BR_IZBD_DCT = models.DecimalField('Retail Brand AWP Discount (including ZBDs)',max_digits=6, decimal_places=3, default=0)
    GUAR_GM_EZBD_DCT = models.DecimalField('Mail Generic AWP Discount (excluding ZBDs)',max_digits=6, decimal_places=3, default=0)
    GUAR_GM_IZBD_DCT = models.DecimalField('Mail Generic AWP Discount (including ZBDs)',max_digits=6, decimal_places=3, default=0)
    GUAR_GR_EZBD_DCT = models.DecimalField('Retail Generic AWP Discount (excluding ZBDs)',max_digits=6, decimal_places=3, default=0)
    GUAR_GR_IZBD_DCT = models.DecimalField('Retail Generic AWP Discount (including ZBDs)',max_digits=6, decimal_places=3, default=0)
    GUAR_MAIL_REBATE = models.CharField('Guarantee Mail Rebate',max_length=15,choices=DROP_DOWN_MENU_42,default="TBD")
    GUAR_R90_REBATE = models.CharField('Guarantee Retail 90 Rebate',max_length=15,choices=DROP_DOWN_MENU_42,default="TBD")
    GUAR_RETAIL_REBATE = models.CharField('Guarantee Retail Rebate',max_length=15,choices=DROP_DOWN_MENU_42,default="TBD")
    GUAR_SPC_BR_DCT = models.DecimalField('Specialty Brand AWP Discount - Retail',max_digits=6, decimal_places=3, default=0)
    GUAR_SPC_GR_DCT = models.DecimalField('Specialty Generic AWP Discount - Retail',max_digits=6, decimal_places=3, default=0)
    GUAR_SPC_M_REBATE = models.CharField('Guarantee Specialty Mail Rebate',max_length=15,choices=DROP_DOWN_MENU_42,default="TBD")
    GUAR_SPC_R_REBATE = models.CharField('Guarantee Specialty Retail Rebate',max_length=15,choices=DROP_DOWN_MENU_42,default="TBD")
    GUAR_SPC_SRX_B_DCT = models.DecimalField('Specialty Brand AWP Discount - SRx',max_digits=6, decimal_places=3, default=0)
    GUAR_SPC_SRX_G_DCT = models.DecimalField('Specialty Generic AWP Discount - SRx',max_digits=6, decimal_places=3, default=0)
    #RETAIL_90_MAIL_RATES = models.CharField('Retail-90/Retail at Mail Rates',max_length=50,choices=DROP_DOWN_MENU_23_CHOICES)
    RETAIL_90_MAIL_RATES_B = models.CharField('Brand Retail-90/Retail at Mail Rates', max_length=50, choices=DROP_DOWN_MENU_23_CHOICES)
    #IF RETAIL_90_MAIL_RATES_B = 'N' THEN GUAR_BR90_EZBD_DCT, GUAR_BR90_IZBD_DCT, GUAR_BR90_DISP_FEE, RETAIL_90_MAIL_RATES_B_DS disappear
    GUAR_BR90_EZBD_DCT = models.DecimalField('Retail-90 Brand AWP Discount (excluding ZBDs)', max_digits=6,decimal_places=3, default=0)
    GUAR_BR90_IZBD_DCT = models.DecimalField('Retail-90 Brand AWP Discount (including ZBDs)', max_digits=6,decimal_places=3, default=0)
    GUAR_BR90_DISP_FEE = models.DecimalField('Retail-90 Brand Dispensing Fee',max_digits=6, decimal_places=3, default=0)
    RETAIL_90_MAIL_RATES_B_DS = models.IntegerField('Retail-90/Retail at Mail Rates Brand Days Supply Breakout',default=0)
    #end RETAIL_90_MAIL_RATES_B dependnet fields
    RETAIL_90_MAIL_RATES_G = models.CharField('Generic Retail-90/Retail at Mail Rates', max_length=50, choices=DROP_DOWN_MENU_23_CHOICES)
    # IF RETAIL_90_MAIL_RATES_G = 'N' THEN GUAR_GR90_EZBD_DCT, GUAR_GR90_IZBD_DCT, GUAR_GR90_DISP_FEE, RETAIL_90_MAIL_RATES_G_DS disappear
    GUAR_GR90_EZBD_DCT = models.DecimalField('Retail-90 Generic AWP Discount (excluding ZBDs)', max_digits=6,decimal_places=3, default=0)
    GUAR_GR90_IZBD_DCT = models.DecimalField('Retail-90 Generic AWP Discount (including ZBDs)', max_digits=6,decimal_places=3, default=0)
    GUAR_GR90_DISP_FEE = models.DecimalField('Retail-90 Generic Dispensing Fee',max_digits=6, decimal_places=3, default=0)
    RETAIL_90_MAIL_RATES_G_DS = models.IntegerField('Retail-90/Retail at Mail Rates Generic Days Supply Breakout',default=0)
    #end RETAIL_90_MAIL_RATES_G dependnet fields
    RETAIL_REBATE_TYPE = models.CharField('Retail Rebate Type',max_length=15,choices=DROP_DOWN_MENU_42,default="TBD")
    RETAIL_SPC_REBATE_TYPE = models.CharField('Retail Specialty Rebate Type',max_length=15,choices=DROP_DOWN_MENU_42,default="TBD")
    GUAR_BM_DISP_FEE = models.DecimalField('Mail Brand Dispensing Fee',max_digits=6, decimal_places=3, default=0)
    GUAR_BR_DISP_FEE = models.DecimalField('Retail Brand Dispensing Fee',max_digits=6, decimal_places=3, default=0)
    GUAR_GM_DISP_FEE = models.DecimalField('Mail Generic Dispensing Fee',max_digits=6, decimal_places=3, default=0)
    GUAR_GR_DISP_FEE = models.DecimalField('Retail Generic Dispensing Fee',max_digits=6, decimal_places=3, default=0)
    GUAR_SPC_B_SRX_DISP_FEE = models.DecimalField('Specialty Brand Dispensing Fee - SRx',max_digits=6, decimal_places=3, default=0)
    GUAR_SPC_BR_DISP_FEE = models.DecimalField('Specialty Brand Dispensing Fee - Retail',max_digits=6, decimal_places=3, default=0)
    GUAR_SPC_G_SRX_DISP_FEE = models.DecimalField('Specialty Generic Dispensing Fee - SRx',max_digits=6, decimal_places=3, default=0)
    GUAR_SPC_GR_DISP_FEE = models.DecimalField('Specialty Generic Dispensing Fee - Retail',max_digits=6, decimal_places=3, default=0)
    GUAR_MAIL_ADMIN_FEE = models.DecimalField('Mail Admin Fee',max_digits=6, decimal_places=3, default=0)
    GUAR_R90_ADMIN_FEE = models.DecimalField('Retail-90 Admin Fee',max_digits=6, decimal_places=3, default=0)
    GUAR_RETAIL_ADMIN_FEE = models.DecimalField('Retail Admin Fee',max_digits=6, decimal_places=3, default=0)
    GUAR_SPC_RETAIL_ADMIN_FEE = models.DecimalField('Specialty Admin Fee - Retail',max_digits=6, decimal_places=3, default=0)
    GUAR_SPC_SRX_ADMIN_FEE = models.DecimalField('Specialty Admin Fee - SRx',max_digits=6, decimal_places=3, default=0)
    BIOSIMILAR_DISC = models.CharField('Biosimilar (Effective Discount)',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_ADJUSTMENTS = models.CharField('Adjustments',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_AUTHORIZED_GENERICS = models.CharField('Authorized Generics',max_length=50,choices=DROP_DOWN_MENU_25_CHOICES, default="TBD",help_text="Authorized generics are prescription drugs produced by brand pharmaceutical companies and marketed under a private label, at generic prices. RA identified via Medispan")
    IE_COB_SECONDARY_CLAIMS = models.CharField('COB/Secondary Claims',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_COMPOUNDS = models.CharField('Compounds',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_DAW_5 = models.CharField('DAW 5',max_length=52,choices=DROP_DOWN_MENU_25_CHOICES, default="TBD")
    IE_DMR_CLAIMS = models.CharField('Direct Member Reimbursement (DMR) Claims',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_EXCLUDED_PROVIDERS = models.CharField('Excluded Providers (e.g. VA, I/T/U, nursing home, long-term care, in-house, on-site)',max_length=30,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_GENERICS_UNDER_EXCLUSIVITY = models.CharField('Generics under Exclusivity',max_length=50,choices=DROP_DOWN_MENU_25_CHOICES, default="TBD")
    IE_MAC_BRANDS = models.CharField('MAC Brands ',max_length=50,choices=DROP_DOWN_MENU_25_CHOICES, default="TBD")
    IE_MAC_GENERICS = models.CharField('MAC Generics',max_length=50,choices=DROP_DOWN_MENU_25_CHOICES, default="TBD")
    IE_NON_DRUG_ITEMS = models.CharField('Non Drug Items',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_NON_MAC_GENERICS = models.CharField('Non-MAC Generics',max_length=37,choices=DROP_DOWN_MENU_25_CHOICES, default="TBD")
    IE_OTC = models.CharField('Over-The-Counter (OTC)',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_PATENT_LITIGATED_GENERICS = models.CharField('Patent Litigated Generics',max_length=37,choices=DROP_DOWN_MENU_25_CHOICES, default="TBD")
    IE_PRICING_ERROR_THRESHOLDS = models.CharField('Pricing error thresholds (claims excluded from the analysis)',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_REJECTS = models.CharField('Rejects',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_REVERSALS = models.CharField('Reversals',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_SSG = models.CharField('SSG',max_length=50,choices=DROP_DOWN_MENU_25_CHOICES, default="TBD")
    IE_SUBROGATION = models.CharField('Subrogation',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_UAC = models.CharField('U&C',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    IE_ZBD = models.CharField('ZBD',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    LDD_DISC = models.DecimalField('LDD (Effective Discount)',max_digits=6, decimal_places=3, default=0)
    LDD_REBATE = models.CharField('LDD (Rebates)',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    M_RATE_BREAKOUT = models.IntegerField('Mail Rate Breakout', default=0)
    M_RATES_APPLY_TO_ALL_M = models.CharField('Mail Rates Apply to All Mail Claims',max_length=50,choices=DROP_DOWN_MENU_21_CHOICES, default="TBD")
    MAIL_REBATE_TYPE = models.CharField('Mail Rebate Type',max_length=15,choices=DROP_DOWN_MENU_42, default="TBD")
    MAIL_SPC_REBATE_TYPE = models.CharField('Mail Specialty Rebate Type',max_length=15,choices=DROP_DOWN_MENU_42, default="TBD")
    NON_SPC_CLASSES = MultiSelectField('Therapy Classes Not Considered Specialty',choices=DROP_DOWN_MENU_41,null=True,blank=True)
    OBSOLETE_NDCS = models.CharField('Obsolete NDCs',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES, default="TDB")
    R90_REBATE_TYPE = models.CharField('Retail 90 Rebate Type',max_length=15,choices=DROP_DOWN_MENU_42, default="TBD")
    IS_TEMPLATE = models.BooleanField("Template?",default=False)
    confirmed = models.BooleanField(default=True)

    objects = models.Manager()
    history = HistoryManager()

    @classmethod
    def search(cls, is_template=None, client_name=None, start_date=None, end_date=None):
        '''
        Gets all contracts which start on or before the given end_date and end on or after the 
        given start_date and belonging to a client with a CLIENT_NAME close to client_name.
        '''
        contracts = cls.objects.filter()

        if is_template:
            contracts = contracts.filter(IS_TEMPLATE=is_template)
            
        if client_name:
            contracts = contracts.filter(CLIENT__CLIENT_NAME__icontains=client_name)

        if start_date:
            contracts = contracts.filter(END_DATE__gte=start_date)

        if end_date:
            contracts = contracts.filter(START_DATE__lte=end_date)
        

        return contracts

    def get_subsequent_contracts(self, number_of_contracts):
        '''
        Gets the specified number of non template subsequent contracts.
        If no contracts are found, new ones are instantiated.
        '''
        contracts = cfd.objects.filter(CLIENT=self.CLIENT, START_DATE__gt=self.START_DATE, IS_TEMPLATE=False).order_by('START_DATE')[:number_of_contracts]
        contracts = list(contracts)

        if len(contracts) < number_of_contracts:
            number_of_new_contracts = number_of_contracts - len(contracts)
            year_gap = len(contracts)
                        
            new_contracts = [cfd(CLIENT=self.CLIENT, 
                            START_DATE=self.START_DATE+relativedelta(years=count + 1 + year_gap), 
                            END_DATE=self.END_DATE+relativedelta(years=count + 1 + year_gap)) for count in range(number_of_new_contracts)]

            contracts.extend(new_contracts)

        return contracts
    
    def get_changed_fields(self):
        '''
        Returns a dict with the changed fields
        as keys and tuples in the format (OLD_VALUE, NEW_VALUE)
        as the values and an empty dict for new instances
        or one with no changes
        '''
        if not self.pk:
            return {}
        
        manager = self.__class__._default_manager
        saved_fields = manager.filter(pk=self.pk).values().get()

        changed_fields = {}

        for field in saved_fields.keys():

            saved_value = saved_fields[field]
            current_value = getattr(self, field)

            if saved_value != current_value:
                changed_fields[field] = (saved_value, current_value)

        return changed_fields

