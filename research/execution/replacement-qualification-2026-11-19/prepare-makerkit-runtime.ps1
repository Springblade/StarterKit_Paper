param([Parameter(Mandatory)][string]$MakerkitSource)

$ErrorActionPreference = 'Stop'
$source = (Resolve-Path -LiteralPath $MakerkitSource).Path
$revision = '9ff430df9c58516add0136bd01ed800ce551675e'
if ((git -C $source rev-parse HEAD) -ne $revision) { throw 'Makerkit checkout is at a different revision.' }

function Invoke-Docker {
    & docker @args
    if ($LASTEXITCODE -ne 0) { throw "Docker command failed with exit code $LASTEXITCODE." }
}

$ts = Join-Path ([IO.Path]::GetTempPath()) ('paper-makerkit-source-' + [guid]::NewGuid() + '.tar')
try {
    git -C $source archive --format=tar "--output=$ts" HEAD
    if ($LASTEXITCODE -ne 0) { throw 'Could not archive the upstream source.' }
    Invoke-Docker run --pull=never --rm -d --name paper-makerkit-node -p 127.0.0.1:3000:3000 node:24-slim sleep infinity
    Invoke-Docker cp $ts paper-makerkit-node:/tmp/makerkit.tar
    Invoke-Docker exec paper-makerkit-node mkdir -p /work
    Invoke-Docker exec paper-makerkit-node tar -xf /tmp/makerkit.tar -C /work
    Invoke-Docker exec -w /work -e CI=true paper-makerkit-node npm exec --yes --package=pnpm@11.18.0 -- pnpm install --frozen-lockfile
    $authRelay = "const net=require('net'); net.createServer(client=>{const server=net.connect(54321,'host.docker.internal'); client.on('error',()=>server.destroy()); server.on('error',()=>client.destroy()); client.pipe(server).pipe(client);}).listen(54321,'127.0.0.1');"
    $appRelay = "const os=require('os'),net=require('net'); const ip=os.networkInterfaces().eth0.find(x=>x.family==='IPv4').address; net.createServer(client=>{const server=net.connect(3000,'::1'); client.on('error',()=>server.destroy()); server.on('error',()=>client.destroy()); client.pipe(server).pipe(client);}).listen(3000,ip);"
    Invoke-Docker exec -d paper-makerkit-node node -e $authRelay
    Invoke-Docker exec -d paper-makerkit-node node -e $appRelay
} finally {
    if (Test-Path -LiteralPath $ts) { Remove-Item -LiteralPath $ts }
}
