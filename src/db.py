import aiopg.sa
import sqlalchemy as sa


__all__ = ['users', 'karma']

meta = sa.MetaData()


users = sa.Table(
    'users', meta,
    sa.Column('id', sa.Integer, nullable=False),    
    sa.Column('email', sa.String(256), nullable=False),
    sa.Column('password_hash', sa.String(512), nullable=False),
    sa.Column('registration_date', sa.Date, nullable=False),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='users_id_pkey'))

karma = sa.Table(
    'karma', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('users_id', sa.Integer, nullable=False),
    sa.Column('karma', sa.Integer, server_default="0", nullable=False),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='karma_id_pkey'),
    sa.ForeignKeyConstraint(['users_id'], [users.c.id],
                            name='karma_users_id_fkey',
                            ondelete='CASCADE'),
)


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=app.loop)
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def get_karma_by_user_id(conn, user_id):
    result = await conn.execute(
        question.select()
        .where(question.c.id == question_id))
    question_record = await result.first()
    if not question_record:
        msg = "Question with id: {} does not exists"
        raise RecordNotFound(msg.format(question_id))
    result = await conn.execute(
        choice.select()
        .where(choice.c.question_id == question_id)
        .order_by(choice.c.id))
    choice_recoreds = await result.fetchall()
    return question_record, choice_recoreds


async def up_karma(conn, question_id, choice_id):
    result = await conn.execute(
        choice.update()
        .returning(*choice.c)
        .where(choice.c.question_id == question_id)
        .where(choice.c.id == choice_id)
        .values(votes=choice.c.votes+1))
    record = await result.fetchone()
    if not record:
        msg = "Question with id: {} or choice id: {} does not exists"
        raise RecordNotFound(msg.format(question_id, choice_id))

async def down_karma(conn, question_id, choice_id):
    result = await conn.execute(
        choice.update()
        .returning(*choice.c)
        .where(choice.c.question_id == question_id)
        .where(choice.c.id == choice_id)
        .values(votes=choice.c.votes+1))
    record = await result.fetchone()
    if not record:
        msg = "Question with id: {} or choice id: {} does not exists"
        raise RecordNotFound(msg.format(question_id, choice_id))
