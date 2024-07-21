# coding=utf-8

from ctr4ever.tests.integration.integrationtest import IntegrationTest
from ctr4ever.tests.mockmodel import MockModelRepository, Base


class ModelRepositoryTest(IntegrationTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with cls.app.app_context():
            Base.metadata.create_all(cls.db.engine)

    def setUp(self):
        self.model_repository = MockModelRepository(self.db)

        with self.app.app_context():
            self.model_repository.delete_all()

    def test_can_create_model(self):
        with self.app.test_request_context():
            crash = self.model_repository.create(name='Crash', description='Bandicoot', value=9000)

            self.assertEqual(crash.name, 'Crash')
            self.assertEqual(crash.description, 'Bandicoot')
            self.assertEqual(crash.value, 9000)

    def test_can_find_one_model_by_id(self):
        with self.app.test_request_context():
            coco = self.model_repository.create(name='Coco', description='Bandicoot', value=8000)

            model = self.model_repository.find_one(coco.id)

            self.assertEqual(model.id, coco.id)
            self.assertEqual(model.name, 'Coco')
            self.assertEqual(model.description, 'Bandicoot')
            self.assertEqual(model.value, 8000)

    def test_can_find_model_by_attributes(self):
        with self.app.test_request_context():
            polar = self.model_repository.create(name='Polar', description='Bear', value=1000)

            models = self.model_repository.find_by(name='Polar')

            self.assertEqual(len(models), 1)

            model = models[0]

            self.assertEqual(model.id, polar.id)
            self.assertEqual(model.name, 'Polar')
            self.assertEqual(model.description, 'Bear')
            self.assertEqual(model.value, 1000)

    def test_can_find_model_and_ignore_none_values(self):
        with self.app.test_request_context():
            crash = self.model_repository.create(name='Crash', description='Bandicoot', value=9000)
            coco = self.model_repository.create(name='Coco', description='Bandicoot', value=8000)

            models = self.model_repository.find_by(description='Bandicoot', name=None)

            self.assertEqual(len(models), 2)
            self.assertEqual(models[0].id, crash.id)
            self.assertEqual(models[1].id, coco.id)

    def test_can_find_model_with_limit(self):
        with self.app.test_request_context():
            crash = self.model_repository.create(name='Crash', description='Bandicoot', value=9000)
            coco = self.model_repository.create(name='Coco', description='Bandicoot', value=8000)

            models = self.model_repository.find_by(description='Bandicoot', limit=1)

            self.assertEqual(len(models), 1)
            self.assertEqual(models[0].id, crash.id)

    def test_can_find_model_with_offset(self):
        with self.app.test_request_context():
            crash = self.model_repository.create(name='Crash', description='Bandicoot', value=9000)
            coco = self.model_repository.create(name='Coco', description='Bandicoot', value=8000)

            models = self.model_repository.find_by(description='Bandicoot', offset=1)

            self.assertEqual(len(models), 1)
            self.assertEqual(models[0].id, coco.id)

    def test_can_not_find_model_with_invalid_attribute(self):
        with self.app.test_request_context():
            self.model_repository.create(name='Crash', description='Bandicoot', value=9000)
            self.model_repository.create(name='Coco', description='Bandicoot', value=8000)

            models = self.model_repository.find_by(description='test', value=2000)
            self.assertEqual(len(models), 0)

    def test_can_not_find_model_with_not_existing_attribute(self):
        with self.app.test_request_context():
            with self.assertRaises(ValueError):
                self.model_repository.find_by(test='test')

    def test_can_count_models(self):
        with self.app.test_request_context():
            self.model_repository.create(name='Crash', description='Bandicoot', value=9000)
            self.model_repository.create(name='Coco', description='Bandicoot', value=8000)

            count = self.model_repository.count()
            self.assertEqual(count, 2)

    def test_can_count_models_by_attributes(self):
        with self.app.test_request_context():
            crash = self.model_repository.create(name='Crash', description='Bandicoot', value=9000)
            coco = self.model_repository.create(name='Coco', description='Bandicoot', value=8000)

            count = self.model_repository.count(value=8000)
            self.assertEqual(count, 1)

    def test_can_count_and_ignore_none_values(self):
        with self.app.test_request_context():
            crash = self.model_repository.create(name='Crash', description='Bandicoot', value=9000)
            coco = self.model_repository.create(name='Coco', description='Bandicoot', value=8000)

            count = self.model_repository.count(description='Bandicoot', name=None)
            self.assertEqual(count, 2)

    def test_can_not_count_models_with_invalid_attribute(self):
        with self.app.test_request_context():
            crash = self.model_repository.create(name='Crash', description='Bandicoot', value=9000)

            count = self.model_repository.count(description='test', value=2000)
            self.assertEqual(count, 0)

    def test_can_not_count_models_with_not_existing_attribute(self):
        with self.app.test_request_context():
            with self.assertRaises(ValueError):
                self.model_repository.count(test='test', value=2000)

    def test_can_update_model(self):
        with self.app.test_request_context():
            crash = self.model_repository.create(name='Crash', description='Bandicoot', value=9000)
            self.model_repository.update(id=crash.id, value=10000)

            model = self.model_repository.find_one(crash.id)

            self.assertEqual(model.value, 10000)

    def test_can_not_update_model_without_id(self):
        with self.app.test_request_context():
            with self.assertRaises(ValueError):
                self.model_repository.update(value=10000)

    def test_can_not_update_model_with_not_existing_attribute(self):
        with self.app.test_request_context():
            crash = self.model_repository.create(name='Crash', description='Bandicoot', value=9000)

            with self.assertRaises(ValueError):
                self.model_repository.update(id=crash.id, test='test')

    def test_can_delete_all_models(self):
        with self.app.test_request_context():
            crash = self.model_repository.create(name='Crash', description='Bandicoot', value=9000)
            coco = self.model_repository.create(name='Coco', description='Bandicoot', value=8000)

            self.model_repository.delete_all()
            count = self.model_repository.count()

            self.assertEqual(count, 0)
