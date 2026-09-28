/* Scene chat (Step 11): the parts the server cannot do for the browser.
 *
 * Posts, notices and form regions arrive as server-rendered HTML over htmx's
 * ws extension and are swapped out of band; this file never builds markup.
 * It shows the connection state, asks for missed posts on every (re)connect,
 * posts over plain HTTP while the socket is down, drops duplicate posts and
 * keeps posts in id order, and sends on Enter (Shift+Enter for a newline).
 */
(function () {
    'use strict';

    // Close codes the server uses on purpose; the extension does not retry them.
    var CLOSED = {
        1000: 'Live updates have ended.',
        4400: 'This page is out of date. Reload it to keep chatting.',
        4403: 'Live updates are unavailable. Reload the page.'
    };

    var socketOpen = false;
    var scrollTo = null;

    function postId(element) {
        return parseInt(element.getAttribute('data-post-id'), 10);
    }

    function pagePosts() {
        return Array.prototype.slice.call(
            document.querySelectorAll('#posts-container [data-post-id]')
        );
    }

    function lastPostId() {
        return pagePosts().reduce(function (max, post) {
            return Math.max(max, postId(post));
        }, 0);
    }

    function setState(live, state, text) {
        live.setAttribute('data-ws-state', state);
        var box = document.getElementById('connection-status');
        var label = document.getElementById('status-indicator');
        if (box && label) {
            label.textContent = text;
            box.hidden = !text;
        }
    }

    function setBusy(busy) {
        var form = document.getElementById('post-form');
        var button = document.getElementById('post-submit-btn');
        if (form && busy) {
            form.setAttribute('aria-busy', 'true');
        } else if (form) {
            form.removeAttribute('aria-busy');
        }
        if (button) {
            button.disabled = busy;
        }
    }

    function liveRoot(event) {
        return event.target.closest && event.target.closest('[data-scene-live]');
    }

    document.addEventListener('htmx:wsConnecting', function (event) {
        var live = liveRoot(event);
        if (live && live.getAttribute('data-ws-state') !== 'connecting') {
            setState(live, 'connecting', 'Reconnecting…');
        }
    });

    document.addEventListener('htmx:wsOpen', function (event) {
        var live = liveRoot(event);
        if (!live) {
            return;
        }
        socketOpen = true;
        setState(live, 'open', '');
        // Posts made since the page rendered, or while the socket was down.
        event.detail.socketWrapper.send(JSON.stringify({ action: 'sync', after: lastPostId() }));
    });

    document.addEventListener('htmx:wsClose', function (event) {
        var live = liveRoot(event);
        if (!live) {
            return;
        }
        socketOpen = false;
        setBusy(false);
        var code = event.detail.event.code;
        setState(live, CLOSED[code] ? 'closed' : 'reconnecting',
            CLOSED[code] || 'Connection lost. Reconnecting…');
    });

    // While the socket is down, post the form to its HTTP action instead of
    // queueing the message (htmx has already cancelled the native submit).
    // The CSRF token is for that HTTP action only; the socket never needs it.
    // (hx-params cannot drop it: htmx 2.0.11's filterValues expects FormData,
    // and the ws extension passes a plain object.)
    document.addEventListener('htmx:wsConfigSend', function (event) {
        var form = event.target;
        if (form.id !== 'post-form') {
            return;
        }
        if (!socketOpen) {
            event.preventDefault();
            form.submit();
            return;
        }
        delete event.detail.parameters.csrfmiddlewaretoken;
    });

    document.addEventListener('htmx:wsAfterSend', function (event) {
        if (event.target.id === 'post-form') {
            setBusy(true);
        }
    });

    document.addEventListener('htmx:wsAfterMessage', function (event) {
        // Every reply to a post carries the notice region; broadcasts of
        // other people's posts do not.
        if (event.detail.message.indexOf('id="scene-chat-notice"') !== -1) {
            setBusy(false);
        }
        if (scrollTo !== null) {
            var post = document.getElementById('post-' + scrollTo);
            scrollTo = null;
            if (post) {
                post.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }
        }
    });

    // A sync reply and a live broadcast can carry the same post, and two
    // posts made at once can arrive in either order.
    document.addEventListener('htmx:oobBeforeSwap', function (event) {
        if (!event.detail.target || event.detail.target.id !== 'posts-container') {
            return;
        }
        var incoming = event.detail.fragment.querySelectorAll('[data-post-id]');
        Array.prototype.forEach.call(incoming, function (post) {
            var id = postId(post);
            if (document.getElementById('post-' + id)) {
                post.remove();
                return;
            }
            scrollTo = id;
            var later = pagePosts().filter(function (existing) {
                return postId(existing) > id;
            })[0];
            if (later) {
                later.parentNode.insertBefore(post, later);
            }
        });
    });

    // "Show earlier posts" must get the posts fragment; anything else (an
    // expired session's login page, an error) loads as a whole page.
    document.addEventListener('htmx:beforeSwap', function (event) {
        var link = event.detail.elt;
        if (link && link.id === 'earlier-posts' &&
                event.detail.xhr.getResponseHeader('TG-Fragment') !== 'scene-posts') {
            event.detail.shouldSwap = false;
            window.location.assign(link.href);
        }
    });

    document.addEventListener('keydown', function (event) {
        var field = event.target;
        if (field.id !== 'message-input' || event.key !== 'Enter' || event.shiftKey ||
                event.isComposing) {
            return;
        }
        event.preventDefault();
        var button = document.getElementById('post-submit-btn');
        if (field.form && !(button && button.disabled)) {
            field.form.requestSubmit();
        }
    });
})();
