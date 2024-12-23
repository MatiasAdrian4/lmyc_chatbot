from service.lmyc_client import LMYCClient, Sale


class TestLMYCClient:
    def test_search_by_date_range(self):
        lmyc_client = LMYCClient()

        assert lmyc_client.get_sales("25/07/2024", "11/08/2024") == [
            Sale(id=40, description="Sale 40", date="25/07/2024", price=89.12),
            Sale(id=41, description="Sale 41", date="30/07/2024", price=45.67),
            Sale(id=42, description="Sale 42", date="02/08/2024", price=78.34),
            Sale(id=43, description="Sale 43", date="03/08/2024", price=12.89),
            Sale(id=44, description="Sale 44", date="11/08/2024", price=56.23),
        ]

    def test_search_by_date_range_and_category(self):
        lmyc_client = LMYCClient()

        assert lmyc_client.get_sales("01/03/2024", "20/09/2024", "Baterias") == [
            Sale(id=11, description="Sale 11", date="01/03/2024", price=12.89),
            Sale(id=31, description="Sale 31", date="04/06/2024", price=23.45),
            Sale(id=51, description="Sale 51", date="19/09/2024", price=12.89),
        ]
