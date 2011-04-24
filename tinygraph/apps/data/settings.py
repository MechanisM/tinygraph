from django.conf import settings

NON_INCREMENTAL_DATA_VALUE_TYPES = getattr(settings, 
    'NON_INCREMENTAL_DATA_VALUE_TYPES', (
    
    'integer',
    'bit_string',
    'octet_string',
    'null',
    'object_identifier',
    'sequence',
    'ip_address',
))

DATA_VALUE_TYPES = getattr(settings, 'DATA_VALUE_TYPES', (
    # Primitive ASN.1 Types
    ('integer', 'Integer'),
    ('bit_string', 'Bit String'),
    ('octet_string', 'Octet String'),
    ('null', 'Null'),
    ('object_identifier', 'Object Identifier'),
    
    # Constructed ASN.1 Types
    ('sequence', 'Sequence'),
    
    # Primitive SNMP Application Types
    ('ip_address', 'IP Address'),
    ('counter', 'Counter'),
    ('gauge', 'Gauge'),
    ('time_ticks', 'Time Ticks'),
    ('opaque', 'Opaque'),
    ('nsap_address', 'Nsap Address'),
))