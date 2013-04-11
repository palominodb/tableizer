from ttt.models import Server
from utilities.utils import str_to_datetime

def since_string(request):
    return {'since_string': request.session.get('since_string', '72h')}
    
def since_date(request):
    return {'since_date': str_to_datetime(request.session.get('since_string', '72h'))}
    
def servers(request):
    return {'server_objects': Server.objects.all()}
