from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import path
from django.shortcuts import render

from .models import *

class PayToCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'transfer_summ', 'date', 'cheque_image_tag', 'qr_code_tag', 'print_cheque_button')
    readonly_fields = ('cheque_image', 'qr_code')
    actions = ['print_selected_cheques']

    def cheque_image_tag(self, obj):
        if obj.cheque_image:
            return format_html(f'<img src="{obj.cheque_image.url}" width="100" height="50" />')
        return "No Cheque Image"
    cheque_image_tag.short_description = 'Cheque Image'

    def qr_code_tag(self, obj):
        if obj.qr_code:
            return format_html(f'<img src="{obj.qr_code.url}" width="50" height="50" />')
        return "No QR Code"
    qr_code_tag.short_description = 'QR Code'

    def print_cheque_button(self, obj):
        return format_html(f'<a class="button" href="/admin/payment/paytocourse/{obj.id}/print/" target="_blank">Print Cheque</a>')
    print_cheque_button.short_description = 'Print Cheque'
    print_cheque_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/print/', self.admin_site.admin_view(self.print_cheque), name='paytocourse-print'),
        ]
        return custom_urls + urls

    def print_cheque(self, request, pk):
        pay_to_course = self.get_object(request, pk)
        return render(request, 'admin/print_cheque.html', {'pay_to_course': pay_to_course})

    def print_selected_cheques(self, request, queryset):
        cheques_html = ""
        for pay_to_course in queryset:
            cheques_html += render_to_string('admin/print_cheque.html', {'pay_to_course': pay_to_course})
        return render(request, 'admin/print_cheques.html', {'cheques_html': cheques_html})

    print_selected_cheques.short_description = 'Print selected cheques'

admin.site.register(PayToCourse, PayToCourseAdmin)
admin.site.register(AddCashToWallet)
admin.site.register(GiveSalary)
admin.site.register(Discounted_students)