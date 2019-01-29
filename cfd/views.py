from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from cfd.models import cfd

def index(request):
    return HttpResponse("Hello, world. You're at the CFD Management index.")

    
class PostsForm(ModelForm):
    class Meta:
        model = cfd
        fields = '__all__'

    fieldsets = (
            ('Client Information', {
                'fields': ('CLIENT_NAME', 'REMEDY_CLIENT_ID')
            }),
            ('Retail', {
                'classes': ['collapse'],
                'fields': ('GUAR_BR_IZBD_DCT','GUAR_BR_EZBD_DCT','GUAR_GR_IZBD_DCT', 'GUAR_GR_EZBD_DCT','GUAR_BR_DISP_FEE','GUAR_GR_DISP_FEE','GUAR_RETAIL_ADMIN_FEE','GUAR_RETAIL_REBATE')
            }),        
            ('Retail 90', {
                'classes': ['collapse'],
                'fields': ('GUAR_BR90_IZBD_DCT','GUAR_BR90_EZBD_DCT','GUAR_GR90_IZBD_DCT','GUAR_GR90_EZBD_DCT','GUAR_BR90_DISP_FEE','GUAR_GR90_DISP_FEE','GUAR_R90_ADMIN_FEE')
            }),
            ('Mail/Retail at Mail Rates', {
                'classes': ['collapse'],
                'fields': ('GUAR_BM_IZBD_DCT','GUAR_BM_EZBD_DCT','GUAR_GM_IZBD_DCT','GUAR_GM_EZBD_DCT','GUAR_BM_DISP_FEE','GUAR_GM_DISP_FEE','GUAR_MAIL_ADMIN_FEE')
            }),
            ('Specialty', { 
                'classes': ['collapse'],
                'fields': ('GUAR_SPC_BR_DCT','GUAR_SPC_GR_DCT','GUAR_SPC_BR_DISP_FEE','GUAR_SPC_GR_DISP_FEE','GUAR_SPC_RETAIL_ADMIN_FEE','GUAR_SPC_SRX_B_DCT','GUAR_SPC_SRX_G_DCT','GUAR_SPC_G_SRX_DISP_FEE','GUAR_SPC_B_SRX_DISP_FEE','GUAR_SPC_SRX_ADMIN_FEE')}),
            ('PBM Client Credits', {
                'classes': ['collapse'],
                'fields': ('IE_SSG','IE_ZBD','IE_UAC','IE_GENERICS_UNDER_EXCLUSIVITY','IE_AUTHORIZED_GENERICS','IE_PATENT_LITIGATED_GENERICS','IE_MAC_GENERICS','IE_NON_MAC_GENERICS','IE_MAC_BRANDS','IE_ADJUSTMENTS','IE_COB_SECONDARY_CLAIMS','IE_DMR_CLAIMS','IE_EXCLUDED_PROVIDERS','IE_REJECTS','IE_REVERSALS','IE_SUBROGATION','IE_NON_DRUG_ITEMS','IE_OTC','IE_PRICING_ERROR_THRESHOLDS','IE_DAW_5','IE_COMPOUNDS','M_RATES_APPLY_TO_ALL_M','M_RATE_BREAKOUT','LDD_DISC','LDD_REBATE','BIOSIMILAR_DISC','OBSOLETE_NDCS')})
            )

@login_required
def post_list(request, template_name='cfd/post_list.html'):
    posts = cfd.objects.all()
    data = {}
    data['object_list'] = posts
    return render(request, template_name, data)

@login_required
def post_create(request, template_name='cfd/post_form.html'):
    form = PostsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cfd:post_list')
    return render(request, template_name, {'form': form})

@login_required
def post_update(request, pk, template_name='cfd/post_form.html'):
    post = get_object_or_404(cfd, pk=pk)
    form = PostsForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('cfd:post_list')
    return render(request, template_name, {'form': form})

@login_required
def post_delete(request, pk, template_name='cfd/post_delete.html'):
    post = get_object_or_404(cfd, pk=pk)
    if request.method=='POST':
        post.delete()
        return redirect('cfd:post_list')
    return render(request, template_name, {'object': post})