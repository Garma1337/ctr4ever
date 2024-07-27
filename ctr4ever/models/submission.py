# coding=utf-8

from marshmallow import Schema, fields
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.model import Model


class SubmissionSchema(Schema):
    id = fields.Int()
    player_id = fields.Int()
    track_id = fields.Int()
    category_id = fields.Int()
    character_id = fields.Int()
    game_version_id = fields.Int()
    ruleset_id = fields.Int()
    platform_id = fields.Int()
    time = fields.Float()
    date = fields.DateTime()
    video = fields.Str()
    comment = fields.Str()
    player = fields.Nested('PlayerSchema', exclude=('submissions',))
    track = fields.Nested('TrackSchema', exclude=('submissions',))
    category = fields.Nested('CategorySchema', exclude=('submissions',))
    character = fields.Nested('CharacterSchema', exclude=('submissions',))
    game_version = fields.Nested('GameVersionSchema', exclude=('submissions',))
    ruleset = fields.Nested('RulesetSchema', exclude=('submissions',))
    platform = fields.Nested('PlatformSchema', exclude=('submissions',))


class Submission(Model):
    __tablename__ = 'submissions'
    __dump_schema__ = SubmissionSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    player_id: Mapped[int] = mapped_column(ForeignKey('players.id'))
    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    game_version_id: Mapped[int] = mapped_column(ForeignKey('game_versions.id'))
    ruleset_id: Mapped[int] = mapped_column(ForeignKey('rulesets.id'))
    platform_id: Mapped[int] = mapped_column(ForeignKey('platforms.id'))
    time: Mapped[int] = Column(Float(2), nullable=False)
    date: Mapped[str] = Column(DateTime(), nullable=False)
    video: Mapped[str] = Column(String(255), nullable=False)
    comment: Mapped[str] = Column(Text(), nullable=True)
    player: Mapped['Player'] = relationship('Player', back_populates='submissions')
    track: Mapped['Track'] = relationship('Track', back_populates='submissions')
    category: Mapped['Category'] = relationship('Category', back_populates='submissions')
    character: Mapped['Character'] = relationship('Character', back_populates='submissions')
    game_version: Mapped['GameVersion'] = relationship('GameVersion', back_populates='submissions')
    ruleset: Mapped['Ruleset'] = relationship('Ruleset', back_populates='submissions')
    platform: Mapped['Platform'] = relationship('Platform', back_populates='submissions')
