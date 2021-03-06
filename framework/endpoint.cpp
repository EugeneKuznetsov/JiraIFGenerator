#include "session.h"
#include "reply.h"
#include "responsestatus.h"
#include "endpoint.h"

Endpoint::Endpoint(const QJSValue &callback, Session *parent, QJSEngine *jsEng, QQmlEngine *qmlEng)
    : QObject(parent)
    , m_headers({{"X-Atlassian-Token", "no-check"}})
    , m_callback(callback)
    , m_session(parent)
    , m_jsEngine(jsEng)
    , m_qmlEngine(qmlEng)
{
}

void Endpoint::setHeader(const QByteArray &header, const QByteArray &value)
{
    m_headers[header] = value;
}

void Endpoint::setBaseUri(const QUrl &uri)
{
    m_baseUri = uri;
}

void Endpoint::setBaseUriQuery(const QUrlQuery &query)
{
    m_baseUri.setQuery(query);
}

Reply *Endpoint::httpPost(const QByteArray &payload)
{
    return adoptReply(m_session->post(m_baseUri, payload, m_headers));
}

Reply *Endpoint::httpGet()
{
    return adoptReply(m_session->get(m_baseUri, m_headers));
}

Reply *Endpoint::httpPut(const QByteArray &payload)
{
    return adoptReply(m_session->put(m_baseUri, payload, m_headers));
}

Reply *Endpoint::httpDelete()
{
    return adoptReply(m_session->deleteResource(m_baseUri, m_headers));
}

void Endpoint::callback(const int statusCode, const QByteArray &data, const QMap<int, bool> &codes, const QJSValueList &arguments)
{
    if (!m_callback.isCallable())
        return;

    ResponseStatus *status = new ResponseStatus(statusCode, data, codes);
    m_qmlEngine->setObjectOwnership(status, QQmlEngine::JavaScriptOwnership);
    QJSValueList argumentsCopy(arguments);
    argumentsCopy.insert(0, m_jsEngine->toScriptValue(status));
    m_callback.call(argumentsCopy);
}

QQmlEngine *Endpoint::getQmlEngine()
{
    return m_qmlEngine;
}

const QJSValue &Endpoint::getCallback() const
{
    return m_callback;
}

void Endpoint::setCallback(const QJSValue &callback)
{
    m_callback = callback;
    emit callbackChanged();
}

Reply *Endpoint::adoptReply(Reply *reply)
{
    reply->setParent(this);
    connect(reply, &Reply::destroy, this, &Endpoint::deleteLater);
    connect(reply, &Reply::networkError, m_session, &Session::networkError);
    return reply;
}
