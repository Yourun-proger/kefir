from dataclasses import dataclass
from kefir import Kefir, Repr


class TestKefirBase:
    def test_basic(self):
        class A:
            def __init__(self, some_attr):
                self.attr = some_attr

        class B:
            def __init__(self, some_attr, some_a_object):
                self.attr = some_attr
                self.a_object = some_a_object

        class BRepr(Repr):
            loads = {"a_object": A}

        kef = Kefir(represents={B: BRepr})
        a_object = A("kefir")
        b_object = B(42, a_object)
        raw_data = {"attr": "some text", "a_object": {"attr": "just attr"}}
        new_obj = kef.load(raw_data, B)

        assert kef.dump(a_object) == {"attr": "kefir"}
        assert kef.dump(b_object) == {"attr": 42, "a_object": {"attr": "kefir"}}
        assert isinstance(new_obj, B)
        assert isinstance(new_obj.a_object, A)

    def test_dataclass(self):
        @dataclass
        class ADataClass:
            attr: str

        @dataclass
        class BDataClass:
            attr: int
            a_object: ADataClass

        kef = Kefir()
        a_object = ADataClass("kefir")
        b_object = BDataClass(42, a_object)

        assert kef.dump(a_object) == {"attr": "kefir"}
        assert kef.dump(b_object) == {"attr": 42, "a_object": {"attr": "kefir"}}

    def test_classes_with_slots(self):
        class AWithSlots:
            __slots__ = ["attr"]

            def __init__(self, some_attr):
                self.attr = some_attr

        class BWithSlots:
            __slots__ = ["attr", "a_object"]

            def __init__(self, some_attr, some_a_object):
                self.attr = some_attr
                self.a_object = some_a_object

        kef = Kefir()
        a_object = AWithSlots("kefir")
        b_object = BWithSlots(42, a_object)

        assert kef.dump(a_object) == {"attr": "kefir"}
        assert kef.dump(b_object) == {"attr": 42, "a_object": {"attr": "kefir"}}
