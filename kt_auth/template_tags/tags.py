import hashlib
from django import template
from rsp.models import RspHiredreq, RspHiredStreamlinereq, HiredreqCompliance
from django.db.models import Q

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
	compliance = HiredreqCompliance.objects.filter(Q(app_id=user_id) & Q(hired_req_id=req_id)).first()
	return compliance

@register.simple_tag
def checkcompliance(user_id):
	compliance = HiredreqCompliance.objects.filter(Q(app_id=user_id)).count()
	return compliance

@register.simple_tag
def get_is_required(check_compliance, compliance, row):
	if check_compliance and compliance is not None:
		return compliance.is_required
	elif not check_compliance and row is not None:
		return row.is_required
	return None

@register.simple_tag
def get_empstatus_hired_req(emp_status):
	data = RspHiredreq.objects.filter(empstatus__name=emp_status, status=1).all()
	return data


@register.simple_tag
def get_empstatus_hired_streamline_req(emp_status):
	data = RspHiredStreamlinereq.objects.filter(empstatus__name=emp_status, status=1).all()
	return data

@register.simple_tag
def get_empstatus_hired_req(emp_status):
	data = RspHiredreq.objects.filter(empstatus__name=emp_status, status=1).all()
	return data

@register.simple_tag(takes_context=True)
def get_session_fullname(context):
	request = context.get('request')
	first_name = request.session.get('user_first_name', '')
	middle_name = request.session.get('user_middle_name', '')
	last_name = request.session.get('user_last_name', '')
	 # Check if there is a middle name and get the initial character followed by a dot
	middle_name_initial = f"{middle_name[0]}." if middle_name else ""
    
    # Concatenate the names with the middle name initial if available
	full_name = f"{first_name} {middle_name_initial} {last_name}".strip()
    
	return full_name