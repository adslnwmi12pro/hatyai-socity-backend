-- Create Admin User for testing
-- Email: admin@hatyai.com
-- Password: admin123456

INSERT INTO users (email, password, username, is_admin, is_subscribed)
VALUES (
    'admin@hatyai.com',
    'scrypt:32768:8:1$dqm9xvFQz3TzYQKp$8f3e5a8e3d8f3e5a8e3d8f3e5a8e3d8f3e5a8e3d8f3e5a8e3d8f3e5a8e3d8f3e5a8e3d8f3e5a8e3d8f3e5a8e3d8',
    'Admin User',
    TRUE,
    TRUE
) ON CONFLICT (email) DO NOTHING;

-- Note: The password hash above is just a placeholder
-- You need to register through the frontend to create a real user with a proper password hash
