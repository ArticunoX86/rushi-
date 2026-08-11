import os
import glob

models_dir = 'app/models'
files = glob.glob(os.path.join(models_dir, '*.py'))

for file in files:
    if os.path.basename(file) in ['__init__.py', 'tenant.py', 'base.py', 'base_model.py']:
        continue
    
    with open(file, 'r') as f:
        content = f.read()
    
    if 'tenant_id' in content:
        continue
        
    lines = content.split('\n')
    
    # inject import if needed
    import_added = False
    for i, line in enumerate(lines):
        if 'import uuid' in line and not import_added:
            lines.insert(i + 1, "from sqlalchemy import ForeignKey")
            import_added = True
            break
            
    # inject after __tablename__
    for i, line in enumerate(lines):
        if '__tablename__ =' in line:
            lines.insert(i + 1, "    tenant_id = mapped_column(ForeignKey('tenants.id'), nullable=True)")
            # also need to import mapped_column if not there? Most have it.
            break
            
    with open(file, 'w') as f:
        f.write('\n'.join(lines))

print("Done updating models")
