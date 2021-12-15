from __future__ import annotations

from dataclasses import field, dataclass
import random
from typing import Type, cast

from faker import Faker
#from faker_airtravel import AirTravelProvider
#from faker_vehicle import VehicleProvider
from data.project.base import Dataset, Entity


# TODO replace this module with your own types

@dataclass
class RentalDataset(Dataset):
    people: list[Person]
    addresses: list[Address]
    jobs: list[Jobs]
    transactions: list[Transaction]

    @staticmethod
    def entity_types() -> list[Type[Entity]]:
        return [Person, Address, Jobs, Transaction]

    @staticmethod
    def from_sequence(entities: list[list[Entity]]) -> Dataset:
        return RentalDataset(
            cast(list[Person], entities[0]),
            cast(list[Address], entities[1]),
            cast(list[Jobs], entities[2]),
            cast(list[Transaction], entities[3])
        )

    def entities(self) -> dict[Type[Entity], list[Entity]]:
        res = dict()
        res[Person] = self.people
        res[Address] = self.addresses
        res[Jobs] = self.jobs
        res[Transaction] = self.transactions

        return res

    @staticmethod
    def generate(
            count_of_customers: int,
            count_of_addresses: int,
            count_of_jobs: int,
            count_of_transactions: int):

        def generate_people(n: int, male_ratio: float = 0.5, locale: str = "en_US",
                            unique: bool = False, min_age: int = 0, max_age: int = 100) -> list[Person]:
            assert n > 0
            assert 0 <= male_ratio <= 1
            assert 0 <= min_age <= max_age

            fake = Faker(locale)
            people = []
            for i in range(n):
                male = random.random() < male_ratio
                generator = fake if not unique else fake.unique
                people.append(Person(
                    "P-" + (str(i).zfill(6)),
                    generator.name_male() if male else generator.name_female(),
                    random.randint(min_age, max_age),
                    male))

            return people

        def generate_addresses(n: int) -> list[Address]:
            assert n > 0

            fake = Faker()
            addresses = []
            for i in range(n):
                addresses.append(Address(fake.address()))

            return addresses

        def generate_jobs(n: int) -> list[Jobs]:
            assert n > 0

            fake = Faker()
            jobs = []
            for i in range(n):


                jobs.append(Jobs(fake.job()))

            return jobs

        def generate_transactions(n: int, people: list[Person], addresses: list[Address], jobs: list[Jobs]) -> list[Transaction]:
            assert n > 0
            assert len(people) > 0
            assert len(addresses) > 0
            assert len(jobs) > 0

            trips = []
            for i in range(n):
                person = random.choice(people)
                address = random.choice(addresses)
                job = random.choice(jobs)
                trips.append(
                    Transaction(f"T-{str(i).zfill(6)}", job.job, person.id,address.address ))

            return trips

        people = generate_people(count_of_customers)
        addresses = generate_addresses(count_of_addresses)
        jobs = generate_jobs(count_of_jobs)
        transactions = generate_transactions(count_of_transactions, people, addresses, jobs)
        return RentalDataset(people, addresses, jobs, transactions)


@dataclass
class Transaction(Entity):
    id: str = field(hash=True)
    job: str = field(repr=True, compare=False)
    person: str = field(repr=True, compare=False)
    address: str = field(repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Transaction:
        return Transaction(seq[0], seq[1], seq[2], seq[3])

    def to_sequence(self) -> list[str]:
        return [self.id, self.job, self.person, self.address]

    @staticmethod
    def field_names() -> list[str]:
        return ["id", "job", "person", "address"]

    @staticmethod
    def collection_name() -> str:
        return "transactions"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Transaction.collection_name()} (
            id VARCHAR(8) NOT NULL PRIMARY KEY,
            job CHAR(4) NOT NULL,
            person VARCHAR(8) NOT NULL,
            address VARCHAR(20) NOT NULL,

            FOREIGN KEY (job) REFERENCES {Jobs.collection_name()}(job),
            FOREIGN KEY (person) REFERENCES {Person.collection_name()}(id),
            FOREIGN KEY (address) REFERENCES {Address.collection_name()}(address)
        );
         """


@dataclass
class Jobs(Entity):
    job: str = field(hash=True)

    @staticmethod
    def from_sequence(seq: list[str]) -> Jobs:
        return Jobs(seq[0])

    def to_sequence(self) -> list[str]:
        return [self.job]

    @staticmethod
    def field_names() -> list[str]:
        return ["job"]

    @staticmethod
    def collection_name() -> str:
        return "jobs"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Jobs.collection_name()} (
            job CHAR(4) NOT NULL PRIMARY KEY
        );
        """


@dataclass
class Address(Entity):
    address: str = field(hash=True, compare=True)

    @staticmethod
    def from_sequence(seq: list[str]) -> Address:
        return Address(seq[0])

    def to_sequence(self) -> list[str]:
        return [self.address]

    @staticmethod
    def field_names() -> list[str]:
        return ["address"]

    @staticmethod
    def collection_name() -> str:
        return "address"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Address.collection_name()} (
            address VARCHAR(20) NOT NULL PRIMARY KEY
        );
        """
@dataclass
class Person(Entity):
    id: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    age: int = field(repr=True, compare=False)
    male: bool = field(default=True, repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Person:
        return Person(seq[0], seq[1], int(seq[2]), bool(seq[3]))

    def to_sequence(self) -> list[str]:
        return [self.id, self.name, str(self.age), str(int(self.male))]

    @staticmethod
    def field_names() -> list[str]:
        return ["id", "name", "age", "male"]

    @staticmethod
    def collection_name() -> str:
        return "people"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Person.collection_name()} (
            id VARCHAR(8) NOT NULL PRIMARY KEY,
            name VARCHAR(50),
            age TINYINT,
            male BOOLEAN
        );
        """