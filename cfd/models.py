from django.db import models

# Create your models here.
class cfd(models.Model):
    class Meta:
            verbose_name = 'Client Financial Record'
            verbose_name_plural = 'Client Financial Records'

    #define drop down values
    #An iterable (e.g., a list or tuple) consisting itself of iterables of exactly two items (e.g. [(A, B), (A, B) ...]) to use as choices for this field. If choices are given, they’re enforced by model validation and the default form widget will be a select box with these choices instead of the standard text field.
#The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name. For example:

    DROP_DOWN_MENU_21_CHOICES = (
        ('Y','Y'),
        ('N','N')
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
        ('Exclude - Assumed by CE','Exclude - Assumed by CE')
    )

    DROP_DOWN_MENU_25_CHOICES = (
        ('Include in GER - Explicit in Contract','Include in GER - Explicit in Contract'),
        ('Include in GER - Assumed by CE','Include in GER - Assumed by CE'),
        ('Include in BER - Explicit in Contract','Include in BER - Explicit in Contract'),
        ('Include in BER - Assumed by CE','Include in BER - Assumed by CE'),
        ('Exclude - Explicit in Contract','Exclude - Explicit in Contract'),
        ('Exclude - Assumed by CE','Exclude - Assumed by CE')
    )

    DROP_DOWN_MENU_26_CHOICES = (
        ('Standard','Standard'),
        ('Reinvested','Reinvested'),
        ('POS','POS')
    )

    DROP_DOWN_MENU_27_CHOICES = (
        ('Standard 2-Tier Qualifying Per Brand Rx','Standard 2-Tier Qualifying Per Brand Rx'),
        ('Standard 2-Tier Qualifying Per Rx','Standard 2-Tier Qualifying Per Rx'),
        ('Standard 2-Tier Non-Qualifying Per Brand Rx','Standard 2-Tier Non-Qualifying Per Brand Rx'),
        ('Standard 2-Tier Non-Qualifying Per Rx','Standard 2-Tier Non-Qualifying Per Rx'),
        ('Standard 3-Tier Qualifying Per Brand Rx','Standard 3-Tier Qualifying Per Brand Rx'),
        ('Standard 3-Tier Qualifying Per Rx','Standard 3-Tier Qualifying Per Rx'),
        ('Standard 3-Tier Non-Qualifying Per Brand Rx','Standard 3-Tier Non-Qualifying Per Brand Rx'),
        ('Standard 3-Tier Non-Qualifying Per Rx','Standard 3-Tier Non-Qualifying Per Rx'),
        ('Reinvested 2-Tier Qualifying Per Brand Rx','Reinvested 2-Tier Qualifying Per Brand Rx'),
        ('Reinvested 2-Tier Qualifying Per Rx','Reinvested 2-Tier Qualifying Per Rx'),
        ('Reinvested 2-Tier Non-Qualifying Per Brand Rx','Reinvested 2-Tier Non-Qualifying Per Brand Rx'),
        ('Reinvested 2-Tier Non-Qualifying Per Rx','Reinvested 2-Tier Non-Qualifying Per Rx'),
        ('Reinvested 3-Tier Qualifying Per Brand Rx','Reinvested 3-Tier Qualifying Per Brand Rx'),
        ('Reinvested 3-Tier Qualifying Per Rx','Reinvested 3-Tier Qualifying Per Rx'),
        ('Reinvested 3-Tier Non-Qualifying Per Brand Rx','Reinvested 3-Tier Non-Qualifying Per Brand Rx'),
        ('Reinvested 3-Tier Non-Qualifying Per Rx','Reinvested 3-Tier Non-Qualifying Per Rx'),
        ('POS 2-Tier Qualifying Per Brand Rx','POS 2-Tier Qualifying Per Brand Rx'),
        ('POS 2-Tier Qualifying Per Rx','POS 2-Tier Qualifying Per Rx'),
        ('POS 2-Tier Non-Qualifying Per Brand Rx','POS 2-Tier Non-Qualifying Per Brand Rx'),
        ('POS 2-Tier Non-Qualifying Per Rx','POS 2-Tier Non-Qualifying Per Rx'),
        ('POS 3-Tier Qualifying Per Brand Rx','POS 3-Tier Qualifying Per Brand Rx'),
        ('POS 3-Tier Qualifying Per Rx','POS 3-Tier Qualifying Per Rx'),
        ('POS 3-Tier Non-Qualifying Per Brand Rx','POS 3-Tier Non-Qualifying Per Brand Rx'),
        ('POS 3-Tier Non-Qualifying Per Rx','POS 3-Tier Non-Qualifying Per Rx'),
        ('Unknown','Unknown')
    )

    DROP_DOWN_MENU_28_CHOICES = (
        ('Offset Within Channel - Explicit in Contract','Offset Within Channel - Explicit in Contract'),
        ('Offset Within Channel - Assumed by CE','Offset Within Channel - Assumed by CE'),
        ('No Offset - Explicit in Contract','No Offset - Explicit in Contract'),
        ('No Offset - Assumed by CE','No Offset - Assumed by CE'),
        ('No Offset Except for Rebates - Explicit in Contract','No Offset Except for Rebates - Explicit in Contract'),
        ('No Offset Except for Rebates - Assumed by CE','No Offset Except for Rebates - Assumed by CE'),
        ('Total Offset Across All Channels - Explicit in Contract','Total Offset Across All Channels - Explicit in Contract'),
        ('Total Offset Across All Channels - Assumed by CE','Total Offset Across All Channels - Assumed by CE'),
        ('Offset by Components Across All Channels - Explicit in Contract','Offset by Components Across All Channels - Explicit in Contract'),
        ('Offset by Components Across All Channels - Assumed by CE','Offset by Components Across All Channels - Assumed by CE')
    )

    DROP_DOWN_MENU_29_CHOICES = (
        ('DAW 2','DAW 2'),
        ('DAW 1 & 2','DAW 1 & 2'),
        ('No DAW','No DAW'),
        ('Unknown','Unknown')
    )

    DROP_DOWN_MENU_30_CHOICES = (
        ('Exclude from non-specialty audit guarantees - Explicit in Contract','Exclude from non-specialty audit guarantees - Explicit in Contract'),
        ('Exclude from non-specialty audit guarantees - Assumed by CE','Exclude from non-specialty audit guarantees - Assumed by CE'),
        ('Include with non-specialty audit guarantees - Explicit in Contract','Include with non-specialty audit guarantees - Explicit in Contract'),
        ('Include with non-specialty audit guarantees - Assumed by CE','Include with non-specialty audit guarantees - Assumed by CE')
    )

    DROP_DOWN_MENU_31_CHOICES = (
        ('Minimum Charge Applies - Explicit in Contract','Minimum Charge Applies - Explicit in Contract'),
        ('Minimum Charge Applies - Assumed by CE','Minimum Charge Applies - Assumed by CE'),
        ('Minimum Charge Does Not Apply - Explicit in Contract','Minimum Charge Does Not Apply - Explicit in Contract'),
        ('Minimum Charge Does Not Apply - Assumed by CE','Minimum Charge Does Not Apply - Assumed by CE')
    )

    DROP_DOWN_MENU_32_CHOICES = (
        ('Per PA','Per PA'),
        ('Per Rx','Per Rx'),
        ('PMPM','PMPM'),
        ('PMPY','PMPY'),
        ('PEPM','PEPM'),
        ('PEPY','PEPY'),
        ('N/A','N/A')
    )

    DROP_DOWN_MENU_34_CHOICES = (
        ('Include in SRx Effective Rate – Explicit in Contract','Include in SRx Effective Rate – Explicit in Contract'),
        ('Include in SRx Effective Rate – Assumed by CE','Include in SRx Effective Rate – Assumed by CE'),
        ('Include in NonSRx Effective Rate – Explicit in Contract','Include in NonSRx Effective Rate – Explicit in Contract'),
        ('Include in NonSRx Effective Rate – Assumed by CE','Include in NonSRx Effective Rate – Assumed by CE'),
        ('Exclude - Explicit in Contract','Exclude - Explicit in Contract'),
        ('Exclude - Assumed by CE','Exclude - Assumed by CE')
    )

    DROP_DOWN_MENU_35_CHOICES = (
        ('Include in BER at IC - Explicit in Contract','Include in BER at IC - Explicit in Contract'),
        ('Include in BER at IC - Assumed by CE','Include in BER at IC - Assumed by CE'),
        ('Include in BER at Penalty Reduced IC - Explicit in Contract','Include in BER at Penalty Reduced IC - Explicit in Contract'),
        ('Include in BER at Penalty Reduced IC - Assumed by CE','Include in BER at Penalty Reduced IC - Assumed by CE'),
        ('Include in GER at Penalty Reduced IC - Explicit in Contract','Include in GER at Penalty Reduced IC - Explicit in Contract'),
        ('Include in GER at Penalty Reduced IC - Assumed by CE','Include in GER at Penalty Reduced IC - Assumed by CE'),
        ('Exclude - Explicit in Contract','Exclude - Explicit in Contract'),
        ('Exclude - Assumed by CE','Exclude - Assumed by CE')
    )

    DROP_DOWN_MENU_36_CHOICES = (
        ('ACA Preventive List','ACA Preventive List'),
        ('CDH Preventive List','CDH Preventive List'),
        ('ACA & CDH Preventive Lists','ACA & CDH Preventive Lists'),
        ('No Preventive List','No Preventive List'),
        ('N/A','N/A')
    )

    DROP_DOWN_MENU_37_CHOICES = (
        ('Y - Mandatory Mail','Y - Mandatory Mail'),
        ('Y - Incentivized Mail','Y - Incentivized Mail'),
        ('Y - Mandatory Mail & Incentivized Mail','Y - Mandatory Mail & Incentivized Mail'),
        ('N - Voluntary Mail','N - Voluntary Mail')
    )

    DROP_DOWN_MENU_38_CHOICES = (
        ('Per Year','Per Year'),
        ('Per Contract Term','Per Contract Term'),
        ('Per Member','Per Member'),
        ('Per Employee','Per Employee'),
        ('N/A','N/A')
    )

    DROP_DOWN_MENU_39_CHOICES = (
        ('OED','OED'),
        ('Drug Level','Drug Level'),
        ('OED & Drug Level ','OED & Drug Level '),
        ('','')
    )

    DROP_DOWN_MENU_40_CHOICES = (
        ('Per Rx','Per Rx'),
        ('PMPM','PMPM'),
        ('PMPY','PMPY'),
        ('PEPM','PEPM'),
        ('PEPY','PEPY')
    )
    
    #define fields
    #format is [database_column_name] = models.[FiedlType]('[Display Name]',[options])
    CLIENT_NAME = models.CharField('Client Name',max_length=255)
    REMEDY_CLIENT_ID = models.IntegerField('REMEDY Client ID',default=0)
    RETAIL_90_MAIL_RATES = models.CharField('Retail-90/Retail at Mail Rates',max_length=13,choices=DROP_DOWN_MENU_23_CHOICES)
    RETAIL_90_MAIL_RATES_B_DS = models.IntegerField('Retail-90/Retail at Mail Rates Brand Days Supply Breakout',default=0)
    RETAIL_90_MAIL_RATES_G_DS = models.IntegerField('Retail-90/Retail at Mail Rates Generic Days Supply Breakout',default=0)
    GUAR_BR_IZBD_DCT = models.DecimalField('Retail Brand AWP Discount (including ZBDs)',max_digits=6, decimal_places=3)
    GUAR_BR_EZBD_DCT = models.DecimalField('Retail Brand AWP Discount (excluding ZBDs)',max_digits=6, decimal_places=3)
    GUAR_GR_IZBD_DCT = models.DecimalField('Retail Generic AWP Discount (including ZBDs)',max_digits=6, decimal_places=3)
    GUAR_GR_EZBD_DCT = models.DecimalField('Retail Generic AWP Discount (excluding ZBDs)',max_digits=6, decimal_places=3)
    GUAR_BR_DISP_FEE = models.DecimalField('Retail Brand Dispensing Fee',max_digits=6, decimal_places=3)
    GUAR_GR_DISP_FEE = models.DecimalField('Retail Generic Dispensing Fee',max_digits=6, decimal_places=3)
    GUAR_RETAIL_ADMIN_FEE = models.DecimalField('Retail Admin Fee',max_digits=6, decimal_places=3)
    GUAR_RETAIL_REBATE = models.DecimalField('     Rebate $',max_digits=6, decimal_places=3)
    GUAR_BR90_IZBD_DCT = models.DecimalField('Retail-90 Brand AWP Discount (including ZBDs)',max_digits=6, decimal_places=3)
    GUAR_BR90_EZBD_DCT = models.DecimalField('Retail-90 Brand AWP Discount (excluding ZBDs)',max_digits=6, decimal_places=3)
    GUAR_GR90_IZBD_DCT = models.DecimalField('Retail-90 Generic AWP Discount (including ZBDs)',max_digits=6, decimal_places=3)
    GUAR_GR90_EZBD_DCT = models.DecimalField('Retail-90 Generic AWP Discount (excluding ZBDs)',max_digits=6, decimal_places=3)
    GUAR_BR90_DISP_FEE = models.DecimalField('Retail-90 Brand Dispensing Fee',max_digits=6, decimal_places=3)
    GUAR_GR90_DISP_FEE = models.DecimalField('Retail-90 Generic Dispensing Fee',max_digits=6, decimal_places=3)
    GUAR_R90_ADMIN_FEE = models.DecimalField('Retail-90 Admin Fee',max_digits=6, decimal_places=3)
    GUAR_BM_IZBD_DCT = models.DecimalField('Mail Brand AWP Discount (including ZBDs)',max_digits=6, decimal_places=3)
    GUAR_BM_EZBD_DCT = models.DecimalField('Mail Brand AWP Discount (excluding ZBDs)',max_digits=6, decimal_places=3)
    GUAR_GM_IZBD_DCT = models.DecimalField('Mail Generic AWP Discount (including ZBDs)',max_digits=6, decimal_places=3)
    GUAR_GM_EZBD_DCT = models.DecimalField('Mail Generic AWP Discount (excluding ZBDs)',max_digits=6, decimal_places=3)
    GUAR_BM_DISP_FEE = models.DecimalField('Mail Brand Dispensing Fee',max_digits=6, decimal_places=3)
    GUAR_GM_DISP_FEE = models.DecimalField('Mail Generic Dispensing Fee',max_digits=6, decimal_places=3)
    GUAR_MAIL_ADMIN_FEE = models.DecimalField('Mail Admin Fee',max_digits=6, decimal_places=3)
    GUAR_SPC_BR_DCT = models.DecimalField('Specialty Brand AWP Discount - Retail',max_digits=6, decimal_places=3)
    GUAR_SPC_GR_DCT = models.DecimalField('Specialty Generic AWP Discount - Retail',max_digits=6, decimal_places=3)
    GUAR_SPC_BR_DISP_FEE = models.DecimalField('Specialty Brand Dispensing Fee - Retail',max_digits=6, decimal_places=3)
    GUAR_SPC_GR_DISP_FEE = models.DecimalField('Specialty Generic Dispensing Fee - Retail',max_digits=6, decimal_places=3)
    GUAR_SPC_RETAIL_ADMIN_FEE = models.DecimalField('Specialty Admin Fee - Retail',max_digits=6, decimal_places=3)
    GUAR_SPC_SRX_B_DCT = models.DecimalField('Specialty Brand AWP Discount - SRx',max_digits=6, decimal_places=3)
    GUAR_SPC_SRX_G_DCT = models.DecimalField('Specialty Generic AWP Discount - SRx',max_digits=6, decimal_places=3)
    GUAR_SPC_G_SRX_DISP_FEE = models.DecimalField('Specialty Generic Dispensing Fee - SRx',max_digits=6, decimal_places=3)
    GUAR_SPC_B_SRX_DISP_FEE = models.DecimalField('Specialty Brand Dispensing Fee - SRx',max_digits=6, decimal_places=3)
    GUAR_SPC_SRX_ADMIN_FEE = models.DecimalField('Specialty Admin Fee - SRx',max_digits=6, decimal_places=3)
    IE_SSG = models.CharField('SSG',max_length=50,choices=DROP_DOWN_MENU_25_CHOICES)
    IE_ZBD = models.CharField('ZBD',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    IE_UAC = models.CharField('U&C',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    IE_GENERICS_UNDER_EXCLUSIVITY = models.CharField('Generics under Exclusivity',max_length=50,choices=DROP_DOWN_MENU_25_CHOICES)
    IE_AUTHORIZED_GENERICS = models.CharField('Authorized Generics',max_length=50,choices=DROP_DOWN_MENU_25_CHOICES)
    IE_PATENT_LITIGATED_GENERICS = models.CharField('Patent Litigated Generics',max_length=37,choices=DROP_DOWN_MENU_25_CHOICES)
    IE_MAC_GENERICS = models.CharField('MAC Generics',max_length=50,choices=DROP_DOWN_MENU_25_CHOICES)
    IE_NON_MAC_GENERICS = models.CharField('Non-MAC Generics',max_length=37,choices=DROP_DOWN_MENU_25_CHOICES)
    IE_MAC_BRANDS = models.CharField('MAC Brands ',max_length=50,choices=DROP_DOWN_MENU_25_CHOICES)
    IE_ADJUSTMENTS = models.CharField('Adjustments',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    IE_COB_SECONDARY_CLAIMS = models.CharField('COB/Secondary Claims',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    IE_DMR_CLAIMS = models.CharField('Direct Member Reimbursement (DMR) Claims',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    IE_EXCLUDED_PROVIDERS = models.CharField('Excluded Providers (e.g. VA, I/T/U, nursing home, long-term care, in-house, on-site)',max_length=30,choices=DROP_DOWN_MENU_24_CHOICES)
    IE_REJECTS = models.CharField('Rejects',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    IE_REVERSALS = models.CharField('Reversals',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    IE_SUBROGATION = models.CharField('Subrogation',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    IE_NON_DRUG_ITEMS = models.CharField('Non Drug Items',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    IE_OTC = models.CharField('Over-The-Counter (OTC)',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    IE_PRICING_ERROR_THRESHOLDS = models.CharField('Pricing error thresholds (claims excluded from the analysis)',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    IE_DAW_5 = models.CharField('DAW 5',max_length=52,choices=DROP_DOWN_MENU_25_CHOICES)
    IE_COMPOUNDS = models.CharField('Compounds',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    M_RATES_APPLY_TO_ALL_M = models.CharField('Mail Rates Apply to All Mail Claims',max_length=50,choices=DROP_DOWN_MENU_21_CHOICES)
    M_RATE_BREAKOUT = models.IntegerField('Mail Rate Breakout')
    LDD_DISC = models.DecimalField('LDD (Effective Discount)',max_digits=6, decimal_places=3)
    LDD_REBATE = models.CharField('LDD (Rebates)',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    BIOSIMILAR_DISC = models.CharField('Biosimilar (Effective Discount)',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)
    OBSOLETE_NDCS = models.CharField('Obsolete NDCs',max_length=50,choices=DROP_DOWN_MENU_24_CHOICES)