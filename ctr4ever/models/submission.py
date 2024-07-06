# coding=utf-8

from marshmallow import Schema, fields
from marshmallow.fields import Nested
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.modelbase import ModelBase


class SubmissionSchema(Schema):

    id = fields.Int()
    player_id = fields.Int()
    track_id = fields.Int()
    category_id = fields.Int()
    character_id = fields.Int()
    game_version_id = fields.Int()
    time = fields.Str()
    date = fields.DateTime()
    video = fields.Str()
    player = Nested('PlayerSchema', exclude=('submissions',))
    track = Nested('TrackSchema', exclude=('submissions',))
    category = Nested('CategorySchema', exclude=('submissions',))
    character = Nested('CharacterSchema', exclude=('submissions',))
    game_version = Nested('GameVersionSchema', exclude=('submissions',))


class Submission(ModelBase):

    __tablename__ = 'submissions'
    __dump_schema__ = SubmissionSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    player_id: Mapped[int] = mapped_column(ForeignKey('players.id'))
    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    game_version_id: Mapped[int] = mapped_column(ForeignKey('game_versions.id'))
    time: Mapped[str] = Column(String(20), nullable=False)
    date: Mapped[str] = Column(DateTime(), nullable=False)
    video: Mapped[str] = Column(String(255), nullable=False)
    player: Mapped['Player'] = relationship('Player', back_populates='submissions')
    track: Mapped['Track'] = relationship('Track', back_populates='submissions')
    category: Mapped['Category'] = relationship('Category', back_populates='submissions')
    character: Mapped['Character'] = relationship('Character', back_populates='submissions')
    game_version: Mapped['GameVersion'] = relationship('GameVersion', back_populates='submissions')
