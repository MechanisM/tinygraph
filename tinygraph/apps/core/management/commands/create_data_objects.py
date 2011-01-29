from django.core.management.base import NoArgsCommand
from pysnmp.smi import builder, view
from tinygraph.apps.core.models import DataObject
from pysnmp.smi.error import NoSuchObjectError

class Command(NoArgsCommand):
    help = 'Creates the DataType enteries in the database, from the python representation of common MIB files created by pysnmp'
    def handle_noargs(self, **options):
        # TODO Find a way to also import OID descriptions from the MIB files,
        #      however the mibViewController doesn't seem to provide access to
        #      this.
        result = raw_input('Are you sure, this will remove existing DataObject enteries (y/N): ')
        if result.lower() != 'y':
            return
        
        print 'OK, This will take a minute or so (there\'s a lot)...'
        mibBuilder = builder.MibBuilder().loadModules()
        mibViewController = view.MibViewController(mibBuilder)
        
        oid, label, sufix = mibViewController.getFirstNodeName()
        
        # Remove existing objects
        DataObject.objects.all().delete()
        
        while True:
            fields = {
                'identifier': '.'.join([str(i) for i in oid]),
                'derived_name': '.'.join([str(i) for i in label]),
            }
            
            try:
                # Ask pysnmp to clarify the what the actual oid of our guessed
                # guessed_parent_oid is.
                guessed_parent_oid = oid[:-1]
                parent_oid, parent_label, parent_suffix = mibViewController.getNodeName(guessed_parent_oid)
                # while parent_oid[-1] == 0:
                #     parent_oid = parent_oid[:-1]
            except (IndexError, NoSuchObjectError):
                # This the root node
                # I think python syntax prevents an IndexError here actually
                pass
            else:
                parent_oid_str = '.'.join([str(i) for i in parent_oid])
                if parent_oid:
                    try:
                        fields['parent'] = DataObject.objects.get(identifier=parent_oid_str)
                    except DataObject.DoesNotExist:
                        print 'WARNING: parent DataObject with oid %s could not be found' % parent_oid_str
                        
            DataObject.objects.create(**fields)
            try:
                oid, label, suffix = mibViewController.getNextNodeName(oid)
            except NoSuchObjectError:
                break