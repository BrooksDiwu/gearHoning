from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    stoneCT = request.args.get("stoneCT", "", type=int)
    leapstoneCT = request.args.get('leapstoneCT', '', type=int)
    stoneP = request.args.get('stoneP', '', type=int)
    leapstoneP = request.args.get('leapstoneP', '', type=int)
    shardCT = request.args.get('shardCT', '', type=int)
    shardP = request.args.get('shardP', '', type=int)
    simpleCT = request.args.get('simpleCT', '', type=int)
    simpleP = request.args.get('simpleP', '', type=int)
    gracePerc = request.args.get('graceCT', '', type=float)
    blessingPerc = request.args.get('blessingCT', '', type=float)
    protectionPerc = request.args.get('protectionCT', '', type=float)
    gold = request.args.get('gold', '', type=int)
    graceP = request.args.get('graceP', '', type=int)
    blessingP = request.args.get('blessingP', '', type=int)
    protectionP = request.args.get('protectionP', '', type=int)
    baseChance = request.args.get('baseChance', '', type=int)

    if baseChance:
        graceCT = 12
        blessingCT = 6
        protectionCT = 2
        
        bestMethod = [0, 0, 0]
        expectedLoss = 9999999999999999
        for i in range(graceCT + 1):
            for j in range(blessingCT + 1):
                for k in range(protectionCT + 1):
                    loss = getExpectedLoss(baseChance, stoneCT, leapstoneCT, shardCT, simpleCT, i, j, k, 
                                        stoneP, leapstoneP, shardP, simpleP, graceP, blessingP, protectionP, gold,
                                        gracePerc, blessingPerc, protectionPerc)
                    if loss < expectedLoss:
                        expectedLoss = loss
                        bestMethod = [i,j,k]

        output = 'Grace: {}     Blessing: {}     Protection: {}'.format(bestMethod[0], bestMethod[1], bestMethod[2])
    else:
        output = ''

    return (
        """<form action="" method="get">
                <input type="number" name="stoneCT"> Blue/Red Stones needed to upgrade <br>
                <input type="number" name="leapstoneCT"> Leapstones needed to upgrade <br>
                <input type="number" name="shardCT"> Shards needed to upgrade <br>
                <input type="number" name="simpleCT"> Simple Oreha needed to upgrade <br>
                <input type="number" name="stoneP"> Current Blue/Red Stone Price <br>
                <input type="number" name="leapstoneP"> Current Leapstone Price <br>
                <input type="number" name="shardP"> Current Shard Price per 1000 <br>
                <input type="number" name="simpleP"> Current Simple Oreha Price <br>
                <input type="number" step='0.01' name="graceCT"> % Added by Grace <br>
                <input type="number" step='0.01' name="blessingCT"> % Added by Blessing <br>
                <input type="number" step='0.01' name="protectionCT"> % Added by Protection <br>
                <input type="number" name="gold"> Gold Cost to Upgrade <br>
                <input type="number" name="graceP"> Solar Grace Price <br>
                <input type="number" name="blessingP"> Solar Blessing Price <br>
                <input type="number" name="protectionP"> Solar Protection Price <br>
                <input type="number" name="baseChance"> Base Upgrade Chance <br>
                <input type="submit" value="Get Optimal Upgrade Enhancers"> 
            </form>"""
        + "Optimal: "
        + output
    )

def getExpectedLoss(baseChance, stoneCT, leapstoneCT, shardCT, simpleCT, graceCT, blessingCT, protectionCT,
                    stoneP, leapstoneP, shardP, simpleP,
                    graceP, blessingP, protectionP, gold, gracePerc, blessingPerc, protectionPerc):
    shardP = shardP/1000
    upgradeTryCost = stoneCT * stoneP + leapstoneCT * leapstoneP + shardCT * shardP + simpleCT * simpleP + gold
    extraCost = graceCT * graceP + blessingCT * blessingP + protectionP * protectionCT
    totalCost = upgradeTryCost + extraCost
    successChance = baseChance + graceCT * gracePerc + blessingCT * blessingPerc + protectionCT * protectionPerc
    if successChance > 100:
        successChance = 100
    return totalCost * (1-successChance*0.01)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)