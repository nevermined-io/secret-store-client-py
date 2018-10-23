pragma solidity 0.4.25;

contract SecretStorePermissions {
    bytes32 forbidden = 0x45ce99addb0f8385bd24f30da619ddcc0cadadab73e2a4ffb7801083086b3fc2;

    function checkPermissions(address user, bytes32 document) constant public returns (bool) {
        if (document == forbidden)
            return false;
        return true;
    }
}
