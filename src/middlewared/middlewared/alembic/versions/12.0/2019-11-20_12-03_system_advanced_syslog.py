"""Move syslog to advanced settings

Revision ID: 350a31cb0769
Revises: ef898631896b
Create Date: 2019-11-20 12:03:35.382256+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '350a31cb0769'
down_revision = 'ef898631896b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('system_advanced', schema=None) as batch_op:
        batch_op.add_column(sa.Column('adv_sysloglevel', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('adv_syslogserver', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('adv_syslog_transport', sa.String(length=12), nullable=True))
        batch_op.add_column(sa.Column('adv_syslog_tls_certificate_id', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_system_advanced_adv_syslog_tls_certificate_id'), ['adv_syslog_tls_certificate_id'], unique=False)
        batch_op.create_foreign_key(batch_op.f('fk_system_advanced_adv_syslog_tls_certificate_id_system_certificate'), 'system_certificate', ['adv_syslog_tls_certificate_id'], ['id'])

    op.execute("UPDATE system_advanced SET adv_sysloglevel = (SELECT stg_sysloglevel FROM system_settings)")
    op.execute("UPDATE system_advanced SET adv_syslogserver = (SELECT stg_syslogserver FROM system_settings)")
    op.execute("UPDATE system_advanced SET adv_syslog_transport = 'UDP'")

    with op.batch_alter_table('system_advanced', schema=None) as batch_op:
        batch_op.alter_column('adv_sysloglevel',
               existing_type=sa.VARCHAR(120),
               nullable=False)
        batch_op.alter_column('adv_syslogserver',
               existing_type=sa.VARCHAR(120),
               nullable=False)
        batch_op.alter_column('adv_syslog_transport',
               existing_type=sa.VARCHAR(12),
               nullable=False)

    with op.batch_alter_table('system_settings', schema=None) as batch_op:
        batch_op.drop_column('stg_sysloglevel')
        batch_op.drop_column('stg_syslogserver')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
