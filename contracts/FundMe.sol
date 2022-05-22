// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe{
    using SafeMathChainlink for uint256;
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }
    function fund() public payable{
        uint256 minimumUSD = 50 * 10 * 18;
        require(msg.value >= minimumUSD, "You need to spend more Eth");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
        // what ETH to USD conversion rate
    }
    function getVersion() public view returns(uint256){
         return priceFeed.version();
    }
    function getPrice() public view returns(uint256){
            (,int256 answer,,,) = priceFeed.latestRoundData();
        // (uint80 roundID, int256 answer, uint256 startedAt, uint256 updatedAt, 
        // uint80 answeredInRound) = priceFeed.latestRoundData();
            return uint256(answer * 10000000000); // returned $ 2,031.68677928
    }   
    function getConversionRate(uint256 ethAmount) public view returns (uint256){
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 100000000;
        return ethAmountInUsd;
    }
    function getBalance() public view returns(uint256){
        return address(this).balance;
    }
    function getEntranceFee() public view returns(uint256){
        //minimum USD
        uint256 minimumUSD = 50 * 10 ** 18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
        }

    modifier onlyOwner{
        require(msg.sender == owner, "You need to be the owner of this contract to withdraw.");
        _;
    }

    function withdraw() payable onlyOwner public {
        msg.sender.transfer(address(this).balance);
        for (uint256 funderIndex=0; funderIndex < funders.length; funderIndex ++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
//  0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
// 0x57A8dd153dcC967960644EEa9beD1612f8931549
// 0x57A8dd153dcC967960644EEa9beD1612f8931549