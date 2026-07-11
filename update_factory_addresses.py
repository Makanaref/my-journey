import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''    const FACTORY_ADDRESSES = {
        lamina1:   "0x569bc0BBda0ecB3963DDc13cd438Bbb8E5f25a01",
        nexus:     "0x0B5d173155Ee7e40d9d568E07B21dff11d7aE2E8",
        ink:       "0x2a126cd72e55c39150092f7D52fd5741999C27E8",
        base:      "0x5f550fe601d9610B1D1977E5b3b5491347ED0418",
        robinhood: "0x620145Db1914c1F9c327FA282BD95b9039647Bc6",
        avax:      "",
        plume:     "0xC37f520dd4926C1dA1e685F35bC0b675AeD8D842",
        zetachain: "0x34ef20427aEf0C0D9de3aafEcb51a9851F876462"
    };'''

new_block = '''    // Base and Robinhood still run the OLD contract (no burn() function) until redeployed.
    const OLD_FACTORY_NETWORKS = ["base", "robinhood"];

    const FACTORY_ADDRESSES = {
        lamina1:   "0x5A923cC58951F731307C73bE6b004503c8c8e17f",
        nexus:     "0x802BeAeC89A61a5e0da9EE05476AC45E40daE13c",
        ink:       "0x1eFfd154CB7adae114F36Af6101a7559c6a98f3F",
        base:      "0x5f550fe601d9610B1D1977E5b3b5491347ED0418",
        robinhood: "0x620145Db1914c1F9c327FA282BD95b9039647Bc6",
        avax:      "0x01d85BF4fb62c2Ba5746e4BC9821E6a7E05d68f4",
        plume:     "0x9791cDBf9a6AF15C313B49d80299769fB8Bd608D",
        zetachain: "0xF988CAc77e456e915aFbDC22BBc8c114fbd4Cd96"
    };'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Factory addresses updated with new burn-capable contracts.")
