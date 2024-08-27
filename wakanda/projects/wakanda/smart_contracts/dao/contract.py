from algopy import *


class Dao(ARC4Contract):
    name: String
    description: String
    end_time: UInt64
    yes_count: UInt64
    no_count: UInt64
    asset_ids: UInt64

    @subroutine
    def has_wakanda_asset(self, sender: Account) -> bool:
        has_asset = False
        asset = Asset(self.asset_ids)
        if asset.balance(sender) > 0:
            has_asset = True

        return has_asset

    @arc4.abimethod(allow_actions=["NoOp"], create="require")
    def create_proposal(
        self, name: String, description: String, end_time: UInt64
    ) -> None:
        self.asset_ids = UInt64(2033034056)
        assert self.has_wakanda_asset(
            Txn.sender
        ), "You must hold one of the required assets to vote"
        assert Global.latest_timestamp > self.end_time, "Voting period has ended"

        self.name = name
        self.description = description
        self.end_time = end_time
        self.yes_count = UInt64(0)
        self.no_count = UInt64(0)

        # self.asset_ids = String(
        #     "2033034056,2002629726,1907988027,1864315348,1853841958,1819525433,1808043536,1743602682,1703181671,1585668221"
        # )

    @arc4.abimethod
    def vote(self, choice: UInt64) -> None:
        assert Global.latest_timestamp < self.end_time, "Voting period has ended"

        # Split asset_ids into a list of asset IDs
        # asset_list = self.asset_ids.split(",")

        # Check if the sender holds any of the specified assets
        assert self.has_wakanda_asset(
            Txn.sender
        ), "You must hold one of the required assets to vote"

        # Count the vote based on the choice
        if choice == 1:
            self.yes_count += 1
        else:
            self.no_count += 1

    @arc4.abimethod
    def delete_proposal(self) -> None:
        assert Txn.sender == Global.creator_address
        asset = Asset(2033034056)
        assert asset.balance(Txn.sender) > 0
