import hashlib
from django import template
from rsp.models import RspHiredreq, RspHiredStreamlinereq

register = template.Library()

@register.filter(name='to_middleinitial')
def to_middleinitial(middlename):
	if middlename != '' and middlename is not None:
		return middlename[0:1].upper() + '.'
	return ''

@register.filter
def range_filter(value):
    return range(1, value)

@register.simple_tag
def getcompliancestreamline(user_id, req_id):
	compliance = OasHiredreqStreamlineCompliance.objects.filter(Q(app_id=user_id) & Q(hired_req_id=req_id)).first()
	return compliance

@register.simple_tag
def getcompliance(user_id, req_id):
	compliance = OasHiredreqCompliance.objects.filter(Q(app_id=user_id) & Q(hired_req_id=req_id)).first()
	return compliance

@register.simple_tag
def get_empstatus_hired_req(emp_status):
	data = RspHiredreq.objects.filter(empstatus__name=emp_status, status=1).all()
	return data


@register.simple_tag
def get_empstatus_hired_streamline_req(emp_status):
	data = RspHiredStreamlinereq.objects.filter(empstatus__name=emp_status, status=1).all()
	return data