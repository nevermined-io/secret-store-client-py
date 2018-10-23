/* global artifacts */
const http = require('http')

const SSPermissions = artifacts.require('./SecretStorePermissions.sol')

module.exports = async function(deployer, network, accounts) {
    // We need to unlock the account to be able to deploy the contract.
    const postData = JSON.stringify({
        method: 'personal_unlockAccount',
        params: [accounts[0], '', null],
        id: 1,
        jsonrpc: '2.0'
    })

    const req = http.request({
        hostname: 'localhost',
        port: '8545',
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    })
    req.write(postData)
    req.end()

    await deployer.deploy(SSPermissions, { from: accounts[0] })
}
