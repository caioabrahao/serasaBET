import { createServer } from 'node:http'
import { parse, fileURLToPath } from 'node:url'
import { join, dirname } from 'node:path'
import { readFile } from 'node:fs'

const root = dirname(fileURLToPath(import.meta.url))

const mimeTypes = {
  'html': 'text/html',
  'css': 'text/css',
  'js': 'text/javascript',
  'svg': 'image/svg+xml',
  'webp': 'image/webp'
}

function file(pathname, response) {
  const path = join(root, pathname)
  const extension = pathname.split('.')[1]

  readFile(path, (err, data) => {
    if (err) {
      response.writeHead(404, { 'Content-Type': 'text/plain' })
      response.end('NOT_FOUND')
    }

    response.writeHead(200, { 'Content-Type': mimeTypes[extension] })
    return response.end(data)
  })
}

function page(pathname, response) {
  const path = pathname === '/'
    ? join(root, '/pages/index.html')
    : join(root, '/pages', pathname + '.html')

  readFile(path, (err, data) => {
    if (err) {
      response.writeHead(404, { 'Content-Type': 'text/plain' })
      return response.end('NOT_FOUND')
    } else {
      response.writeHead(200, { 'Content-Type': 'text/html' })
      return response.end(data)
    }
  })
}

const server = createServer(async (request, response) => {
  const { pathname } = parse(request.url)

  if (pathname.startsWith('/static')) {
    return file(pathname, response)
  }

  const resp = await fetch('http://localhost:5000/refresh-session', {
    method: 'POST',
    headers: {
      'Cookie': request.headers.cookie,
    }
  })

  const setCookie = resp.headers.getSetCookie()
  response.setHeader('Set-Cookie', setCookie)

  const isAuthenticated = resp.status === 201
  const isAuthenticationRoute = ['/login', '/register'].includes(pathname)
  
  if (!isAuthenticated && !isAuthenticationRoute) {
    response.writeHead(301, { location: '/login' })
    return response.end()
  }
  
  if (isAuthenticated && isAuthenticationRoute) {
    response.writeHead(301, { location: '/' })
    return response.end()
  }

  return page(pathname, response)
})

const port = Number(process.env.PORT) || 3000

server.listen(port, '0.0.0.0', () => {
  console.log('Listening on http://0.0.0.0:' + port)
})
